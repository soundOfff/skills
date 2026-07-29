#!/usr/bin/env bash
#
# install.sh — link this repo's skills into the live Claude Code and Codex trees.
#
# The repo is the source of truth. Each skill is symlinked into ~/.claude/skills
# (and, for the Codex subset, ~/.codex/skills) so editing a file here takes
# effect in both tools with no copying and no drift.
#
# Anything real that would be overwritten is moved into a timestamped backup
# directory first — the script never deletes a real file.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_SKILLS="${CLAUDE_SKILLS:-$HOME/.claude/skills}"
CODEX_SKILLS="${CODEX_SKILLS:-$HOME/.codex/skills}"
CLAUDE_AGENTS="${CLAUDE_AGENTS:-$HOME/.claude/agents}"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="$REPO/.install-backup/$STAMP"

DO_CLAUDE=1
DO_CODEX=1
ALL_CODEX=0
DRY=0

usage() {
  cat <<'EOF'
usage: ./install.sh [options]

  --claude-only   link into ~/.claude/skills only
  --codex-only    link into ~/.codex/skills only
  --all-codex     give Codex every skill, not just the codex-skills.txt subset
  --dry-run       print what would happen, change nothing
  -h, --help      this message

Environment overrides: CLAUDE_SKILLS, CODEX_SKILLS
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --claude-only) DO_CODEX=0 ;;
    --codex-only)  DO_CLAUDE=0 ;;
    --all-codex)   ALL_CODEX=1 ;;
    --dry-run)     DRY=1 ;;
    -h|--help)     usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

say()  { printf '%s\n' "$*"; }
step() { printf '\n\033[1m%s\033[0m\n' "$*"; }

# All skill source directories, as "name<TAB>abs_path".
skill_sources() {
  local d
  for d in "$REPO"/skills/*/ "$REPO"/vendor/skills/*/; do
    [ -d "$d" ] || continue
    [ -f "$d/SKILL.md" ] || continue
    printf '%s\t%s\n' "$(basename "$d")" "${d%/}"
  done
}

# link <name> <src> <dest_dir> <backup_label>
#
# backup_label namespaces the backup directory. It cannot be derived from
# destdir, because ~/.claude/skills and ~/.codex/skills share the basename
# "skills" — deriving it would make the second destination's backup nest inside
# the first one's.
link_one() {
  local name="$1" src="$2" destdir="$3" blabel="$4" dest="$destdir/$1"

  # Already pointing where we want it: nothing to do.
  if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$src" ]; then
    return 0
  fi

  if [ $DRY -eq 1 ]; then
    if [ -L "$dest" ]; then say "  relink  $name (was -> $(readlink "$dest"))"
    elif [ -e "$dest" ]; then say "  BACKUP+link  $name (real files present)"
    else say "  link    $name"; fi
    return 0
  fi

  if [ -L "$dest" ]; then
    # A stale symlink carries no content of its own; safe to drop.
    rm "$dest"
  elif [ -e "$dest" ]; then
    # Real files. Preserve them before we take over the path.
    mkdir -p "$BACKUP/$blabel"
    mv "$dest" "$BACKUP/$blabel/$name"
    say "  backed up $name -> ${BACKUP#"$REPO"/}/$blabel/$name"
  fi

  ln -s "$src" "$dest"
}

install_into() {
  local destdir="$1" filter="$2" label="$3" blabel="$4"
  step "$label -> $destdir"
  mkdir -p "$destdir"

  local n=0
  while IFS=$'\t' read -r name src; do
    if [ "$filter" = "subset" ] && ! grep -qxF "$name" "$REPO/codex-skills.txt"; then
      continue
    fi
    link_one "$name" "$src" "$destdir" "$blabel"
    n=$((n + 1))
  done < <(skill_sources)
  say "  $n skill(s) linked"
}

[ $DRY -eq 1 ] && say "DRY RUN — nothing will be changed"

if [ $DO_CLAUDE -eq 1 ]; then
  install_into "$CLAUDE_SKILLS" all "Claude Code" claude-skills
fi

if [ $DO_CODEX -eq 1 ]; then
  if [ $ALL_CODEX -eq 1 ]; then
    install_into "$CODEX_SKILLS" all "Codex (all skills)" codex-skills
  else
    install_into "$CODEX_SKILLS" subset "Codex (codex-skills.txt subset)" codex-skills
  fi
fi

# The single loose agent definition is a file, not a directory.
if [ $DO_CLAUDE -eq 1 ] && [ -f "$REPO/agents/js-ts-interview-drill.md" ]; then
  step "Agents -> $CLAUDE_AGENTS"
  if [ $DRY -eq 1 ]; then
    say "  link    js-ts-interview-drill.md"
  else
    mkdir -p "$CLAUDE_AGENTS"
    dest="$CLAUDE_AGENTS/js-ts-interview-drill.md"
    src="$REPO/agents/js-ts-interview-drill.md"
    if [ -L "$dest" ]; then rm "$dest"
    elif [ -e "$dest" ]; then
      mkdir -p "$BACKUP/agents"; mv "$dest" "$BACKUP/agents/"
      say "  backed up js-ts-interview-drill.md"
    fi
    ln -s "$src" "$dest"
    say "  1 agent linked"
  fi
fi

if [ $DRY -eq 0 ] && [ -d "$BACKUP" ]; then
  step "Backups"
  say "  displaced files kept at: $BACKUP"
fi

step "Done"
say "Config files under config/ are reference copies and are NOT linked;"
say "diff them against ~/.claude and ~/.codex by hand before applying."
