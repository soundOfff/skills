#!/usr/bin/env bash

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
CODEX_DIR="${CODEX_DIR:-$HOME/.codex}"
BACKUP="$REPO/.install-backup/$(date +%Y%m%d-%H%M%S)"
FETCHED="$REPO/.agents/skills"
DOTAGENTS="@sentry/dotagents@3.4.0"

DO_CLAUDE=1
DO_CODEX=1
DO_FETCH=1
DRY=0

usage() {
  cat <<'EOF'
usage: ./install.sh [--dry-run] [--no-fetch] [--claude-only | --codex-only]

  --dry-run      print what would change, change nothing
  --no-fetch     link the third-party skills already fetched, fetch nothing
  --claude-only  link into Claude Code only
  --codex-only   link into Codex only

Targets: $CLAUDE_DIR (default ~/.claude) and $CODEX_DIR (default ~/.codex).
Third-party skills come from agents.toml. Fetching them needs Node 20 or later.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --no-fetch) DO_FETCH=0 ;;
    --claude-only) DO_CODEX=0 ;;
    --codex-only) DO_CLAUDE=0 ;;
    -h | --help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

linked=0 relinked=0 backed_up=0 pruned=0 unchanged=0

say() { printf '%s\n' "$*"; }
act() { [ $DRY -eq 1 ] || "$@"; }

pinned_names() {
  [ -f "$REPO/agents.toml" ] || return 0
  awk '/^\[\[skills\]\]/ { s = 1; next } /^\[/ { s = 0 } s && /^name *= *"/ { sub(/^name *= *"/, ""); sub(/".*$/, ""); print }' "$REPO/agents.toml"
}

fetch_pinned() {
  local out
  say ""
  say "agents.toml -> ${FETCHED#"$REPO"/}"
  if [ $DO_FETCH -eq 0 ]; then
    say "  skip    fetch (--no-fetch)"
  elif [ $DRY -eq 1 ]; then
    say "  fetch   $(pinned_names | wc -l | tr -d ' ') pinned skills with $DOTAGENTS"
  elif ! command -v npx >/dev/null 2>&1; then
    say "  skip    fetch: npx is not on PATH, install Node 20 or later"
  elif out="$(cd "$REPO" && npx --yes "$DOTAGENTS" --project install 2>&1)"; then
    say "  fetched $(pinned_names | wc -l | tr -d ' ') pinned skills"
  else
    printf '%s\n' "$out" | sed 's/^/    /'
    say "  failed  fetch, so only skills fetched before are linked"
  fi
}

skill_sources() {
  local d name
  for d in "$REPO"/skills/*/; do
    [ -f "$d/SKILL.md" ] && printf '%s\t%s\n' "$(basename "$d")" "${d%/}"
  done
  for name in $(pinned_names); do
    if [ -f "$FETCHED/$name/SKILL.md" ] || { [ $DRY -eq 1 ] && [ $DO_FETCH -eq 1 ]; }; then
      printf '%s\t%s\n' "$name" "$FETCHED/$name"
    fi
  done
  return 0
}

unfetched() {
  local name
  [ $DRY -eq 1 ] && [ $DO_FETCH -eq 1 ] && return 0
  for name in $(pinned_names); do
    [ -f "$FETCHED/$name/SKILL.md" ] || printf '%s ' "$name"
  done
  return 0
}

agent_sources() {
  local f
  for f in "$REPO"/agents/"$1"/*."$2"; do
    [ -f "$f" ] && printf '%s\t%s\n' "$(basename "$f")" "$f"
  done
  return 0
}

link_one() {
  local name="$1" src="$2" dest="$3/$1" label="$4"
  if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$src" ]; then
    unchanged=$((unchanged + 1))
    return
  fi
  if [ -L "$dest" ]; then
    say "  relink  $label/$name (was -> $(readlink "$dest"))"
    act rm "$dest"
    relinked=$((relinked + 1))
  elif [ -e "$dest" ]; then
    say "  backup  $label/$name -> ${BACKUP#"$REPO"/}/$label/$name"
    act mkdir -p "$BACKUP/$label"
    act mv "$dest" "$BACKUP/$label/$name"
    backed_up=$((backed_up + 1))
  else
    say "  link    $label/$name"
    linked=$((linked + 1))
  fi
  act ln -s "$src" "$dest"
}

is_listed() { case $'\n'"$2"$'\n' in *$'\n'"$1"$'\n'*) return 0 ;; esac; return 1; }
points_into_kit() { [ "${1#"$REPO"/}" != "$1" ]; }

prune() {
  local dir="$1" label="$2" wanted="$3" entry target name reason
  for entry in "$dir"/* "$dir"/.[!.]*; do
    [ -L "$entry" ] || continue
    name="$(basename "$entry")"
    is_listed "$name" "$wanted" && continue
    target="$(readlink "$entry")"
    if ! points_into_kit "$target"; then
      [ -e "$entry" ] || say "  leave   $label/$name (dangling -> $target, not a kit link)"
      continue
    fi
    if [ -e "$entry" ]; then reason="no longer in the kit"; else reason="dangling -> $target"; fi
    say "  prune   $label/$name ($reason)"
    act rm "$entry"
    pruned=$((pruned + 1))
  done
}

install_set() {
  local dest="$1" label="$2" sources="$3" name src
  say ""
  say "$label -> $dest"
  act mkdir -p "$dest"
  while IFS=$'\t' read -r name src; do
    [ -n "$name" ] && link_one "$name" "$src" "$dest" "$label"
  done <<<"$sources"
  prune "$dest" "$label" "$(printf '%s\n' "$sources" | cut -f1)"
}

[ $DRY -eq 1 ] && say "dry run: nothing will change"

fetch_pinned
skills="$(skill_sources)"
missing="$(unfetched)"
if [ $DO_CLAUDE -eq 1 ]; then
  install_set "$CLAUDE_DIR/skills" claude-skills "$skills"
  install_set "$CLAUDE_DIR/agents" claude-agents "$(agent_sources claude md)"
fi
if [ $DO_CODEX -eq 1 ]; then
  install_set "$CODEX_DIR/skills" codex-skills "$skills"
  install_set "$CODEX_DIR/agents" codex-agents "$(agent_sources codex toml)"
fi

say ""
say "linked $linked, relinked $relinked, backed up $backed_up, pruned $pruned, unchanged $unchanged"
if [ $DRY -eq 0 ] && [ $backed_up -gt 0 ]; then
  say "displaced files are in $BACKUP"
fi
if [ -n "$missing" ]; then
  say "not fetched, so not linked: ${missing% }"
  [ $DO_FETCH -eq 0 ] || exit 1
fi
