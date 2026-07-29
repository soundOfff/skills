#!/usr/bin/env bash
#
# hunter/selftest.sh — exercise the whole fan-out with stubbed CLIs.
#
# Runs in seconds and spends no subscription quota. It verifies the
# orchestration: argument validation, diff assembly, prompt rendering, the
# concurrency matrix, failure accounting, and the consensus hand-off. It says
# nothing about audit quality — only that the machinery is sound.

set -uo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FANOUT="$SKILL_DIR/scripts/fanout.sh"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/hunter-selftest.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT

PASS=0
FAIL=0

ok()   { PASS=$((PASS + 1)); printf '  \033[32mok\033[0m   %s\n' "$1"; }
bad()  { FAIL=$((FAIL + 1)); printf '  \033[31mFAIL\033[0m %s\n' "$1"; [ $# -gt 1 ] && printf '       %s\n' "$2"; }
check() { # description, expected-substring, actual
  case "$3" in *"$2"*) ok "$1" ;; *) bad "$1" "expected to contain: $2" ;; esac
}

# --- stub CLIs ---------------------------------------------------------------

mkdir -p "$TMP/bin"

# claude: prompt arrives after -p; report goes to stdout.
cat > "$TMP/bin/claude" <<'STUB'
#!/bin/sh
prompt=""
while [ $# -gt 0 ]; do
  case "$1" in -p) prompt="$2"; shift 2 ;; *) shift ;; esac
done
if [ -n "${HUNTER_STUB_FAIL:-}" ]; then
  case "$prompt" in *"$HUNTER_STUB_FAIL"*) echo "stub: forced failure" >&2; exit 3 ;; esac
fi
printf '%s\n' "$prompt" > "${HUNTER_STUB_ECHO:-/dev/null}"
printf '## Findings\n\n### COR-1 — stub finding\n\n- **Severity**: low\n'
STUB

# codex: honours -o by writing the report there.
cat > "$TMP/bin/codex" <<'STUB'
#!/bin/sh
out=""
while [ $# -gt 0 ]; do
  case "$1" in -o) out="$2"; shift 2 ;; *) shift ;; esac
done
printf '## Findings\n\n### SUP-1 — stub finding\n\n- **Severity**: low\n' > "$out"
STUB

chmod +x "$TMP/bin/claude" "$TMP/bin/codex"
export PATH="$TMP/bin:$PATH"
export CODEX_BIN="$TMP/bin/codex"

# --- fixture repo ------------------------------------------------------------

# A branch off main with one commit plus uncommitted work, so the diff has to
# span merge-base..worktree rather than just HEAD..worktree.
REPO="$TMP/repo"
mkdir -p "$REPO/src"
git -C "$REPO" init -q
git -C "$REPO" symbolic-ref HEAD refs/heads/main
printf 'const a = 1\n' > "$REPO/src/app.js"
git -C "$REPO" add -A
git -C "$REPO" -c user.email=t@t -c user.name=t commit -qm init
git -C "$REPO" checkout -qb feature
printf 'const b = 2\n' >> "$REPO/src/app.js"   # committed on the branch
git -C "$REPO" -c user.email=t@t -c user.name=t commit -qam second
printf 'const c = 3\n' >> "$REPO/src/app.js"   # uncommitted
REPO="$(cd "$REPO" && pwd)"                    # match the path fanout.sh reports

printf '\nhunter selftest — %s\n\n' "$REPO"

# --- argument validation -----------------------------------------------------

printf 'argument validation\n'

out="$("$FANOUT" --help 2>&1)"; rc=$?
[ $rc -eq 0 ] && check "--help exits 0" "Usage: fanout.sh" "$out" || bad "--help exits 0"

check "rejects -j 0"            "must be at least 1"        "$("$FANOUT" -j 0 -n 2>&1)"
check "rejects -j abc"          "must be a positive integer" "$("$FANOUT" -j abc -n 2>&1)"
check "rejects unknown track"   "unknown track"             "$("$FANOUT" -t bogus -n 2>&1)"
check "rejects unknown model"   "unknown model"             "$("$FANOUT" -m bogus -n 2>&1)"
check "rejects unknown flag"    "unknown option"            "$("$FANOUT" --bogus -n 2>&1)"
check "rejects missing scope-file" "cannot read scope file"  "$("$FANOUT" --scope-file /nope -n 2>&1)"
check "rejects bad --base"      "does not resolve"          "$("$FANOUT" -C "$REPO" --base nope/xyz -n 2>&1)"
check "dedupes selectors"       "2 track(s) x 1 model(s)"   "$("$FANOUT" -t security,security,memory -m gpt,gpt -n 2>&1)"

# --- dry run is inert --------------------------------------------------------

printf '\ndry run\n'

CLEAN="$TMP/clean"; mkdir -p "$CLEAN"
git -C "$CLEAN" init -q
"$FANOUT" -C "$CLEAN" -n >/dev/null 2>&1
[ -z "$(ls -A "$CLEAN" | grep -v '^.git$')" ] \
  && ok "dry run writes nothing" \
  || bad "dry run writes nothing" "created: $(ls -A "$CLEAN")"

check "dry run lists the matrix" "12 audits" "$("$FANOUT" -C "$REPO" -n 2>&1)"

# --- full fan-out ------------------------------------------------------------

printf '\nfan-out\n'

OUT="$TMP/run1"
out="$("$FANOUT" -C "$REPO" -o "$OUT" -t correctness,security --no-report "audit the src directory" 2>&1)"; rc=$?

[ $rc -eq 0 ] && ok "clean run exits 0" || bad "clean run exits 0" "exit $rc"
check "reports all audits ok" "4/4 audits produced a report" "$out"

n="$(ls "$OUT/reports" | wc -l | tr -d ' ')"
[ "$n" = "4" ] && ok "4 reports written" || bad "4 reports written" "got $n"

for f in correctness.claude correctness.gpt security.claude security.gpt; do
  [ -s "$OUT/reports/$f.md" ] && [ "$(cat "$OUT/status/$f")" = "0" ] \
    || bad "report + status for $f"
done
ok "every track x model pair produced a report and a zero status"

# --- prompt rendering --------------------------------------------------------

printf '\nprompt rendering\n'

P="$(cat "$OUT/prompts/correctness.md")"
check "carries the track prompt"  "Correctness and Concurrency"      "$P"
check "carries the scope"         "audit the src directory"          "$P"
check "carries the repo path"     "$REPO"                            "$P"
check "attaches the diff"         "diff.patch"                       "$P"
check "carries the trust block"   "data under audit, not instruction" "$P"

# --out lives outside the repo here, so no exclusion block should appear
case "$P" in
  *"Do not audit"*) bad "no exclusion block when --out is outside the repo" ;;
  *) ok "no exclusion block when --out is outside the repo" ;;
esac

OUT_IN="$TMP/run-inside"
"$FANOUT" -C "$REPO" -t correctness -m claude --no-report >/dev/null 2>&1
INSIDE_PROMPT="$(cat "$REPO"/.hunter/*/prompts/correctness.md)"
check "exclusion block when --out is inside the repo" "Do not audit \`.hunter/\`" "$INSIDE_PROMPT"

# --- diff assembly -----------------------------------------------------------

printf '\ndiff assembly\n'

D="$OUT/diff.patch"
[ -s "$D" ] && ok "diff written" || bad "diff written"

n="$(grep -c '^diff --git a/src/app.js' "$D")"
[ "$n" = "1" ] && ok "single coherent patch per file" || bad "single coherent patch per file" "got $n headers for src/app.js"

grep -q '^+const b' "$D" && ok "diff includes committed change" || bad "diff includes committed change"
grep -q '^+const c' "$D" && ok "diff includes uncommitted change" || bad "diff includes uncommitted change"

check "no-diff is explained" "disabled for this run" \
  "$(cat "$("$FANOUT" -C "$REPO" -o "$TMP/run-nodiff" -t correctness -m claude --no-diff --no-report >/dev/null 2>&1; echo "$TMP/run-nodiff/prompts/correctness.md")")"

# --- output directory safety -------------------------------------------------

printf '\noutput directory\n'

check "refuses a populated --out" "is not empty" \
  "$("$FANOUT" -C "$REPO" -o "$OUT" -t correctness -m claude --no-report 2>&1)"

"$FANOUT" -C "$REPO" -o "$OUT" -t correctness -m claude --no-report --force >/dev/null 2>&1
n="$(ls "$OUT/reports" | wc -l | tr -d ' ')"
[ "$n" = "1" ] && ok "--force clears prior reports" || bad "--force clears prior reports" "got $n"

ln -s /tmp "$TMP/symrepo-hunter" 2>/dev/null
SYM="$TMP/symrepo"; mkdir -p "$SYM"; git -C "$SYM" init -q; ln -s /tmp "$SYM/.hunter"
check "refuses a .hunter symlink" "is a symlink" "$("$FANOUT" -C "$SYM" -t correctness -m claude --no-report 2>&1)"

# --- failure accounting ------------------------------------------------------

printf '\nfailure accounting\n'

out="$(HUNTER_STUB_FAIL="Memory and Resource" "$FANOUT" -C "$REPO" -o "$TMP/run-fail" \
        -t correctness,memory -m claude --no-report 2>&1)"; rc=$?
check "partial failure is reported" "1/2 audits produced a report" "$out"
check "the failing job is named"    "FAIL  memory"                  "$out"
[ $rc -ne 0 ] && ok "partial failure exits non-zero" || bad "partial failure exits non-zero" "exit $rc"

out="$(HUNTER_STUB_FAIL="You are a" "$FANOUT" -C "$REPO" -o "$TMP/run-allfail" \
        -t correctness -m claude --no-report 2>&1)"; rc=$?
check "total failure is fatal" "every audit failed" "$out"
[ $rc -ne 0 ] && ok "total failure exits non-zero" || bad "total failure exits non-zero"

# --- consensus hand-off ------------------------------------------------------

printf '\nconsensus\n'

ECHO="$TMP/judge-prompt.txt"
out="$(HUNTER_STUB_ECHO="$ECHO" "$FANOUT" -C "$REPO" -o "$TMP/run-report" \
        -t correctness,security "scoped run" 2>&1)"; rc=$?

[ $rc -eq 0 ] && ok "run with consensus exits 0" || bad "run with consensus exits 0" "exit $rc"
[ -s "$TMP/run-report/HUNTER-REPORT.md" ] && ok "consensus report written" || bad "consensus report written"

J="$(cat "$ECHO")"
check "judge told the real pair count"  "2 specialt(ies) x 2 model famil(ies) = 4 source pairs" "$J"
check "judge told which specialties"    "Specialties run: correctness security"                 "$J"
check "judge given the reports path"    "run-report/reports/"                                   "$J"
check "judge warned off assuming 6x2"   "Do not assume a full six-by-two run"                    "$J"

out="$(HUNTER_STUB_FAIL="Application Security" HUNTER_STUB_ECHO="$TMP/judge2.txt" \
        "$FANOUT" -C "$REPO" -o "$TMP/run-report2" -t correctness,security -m claude 2>&1)"
check "missing sources disclosed to judge" "security.claude.md\` — MISSING" "$(cat "$TMP/judge2.txt")"

# --- result ------------------------------------------------------------------

printf '\n%s passed, %s failed\n\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ] || exit 1
