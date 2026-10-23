#!/usr/bin/env bash
#
# Link this kit's skills and agents into Claude Code and Codex.
#
# The repo stays the source of truth: every skill and agent is a symlink, so an
# edit here takes effect in both tools at once. Real files that would be
# displaced are moved to .install-backup/<timestamp>/ first, and nothing real is
# ever deleted. Re-running converges on the same state.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
CODEX_DIR="${CODEX_DIR:-$HOME/.codex}"
BACKUP="$REPO/.install-backup/$(date +%Y%m%d-%H%M%S)"

DO_CLAUDE=1
DO_CODEX=1
DRY=0

usage() {
  cat <<'EOF'
usage: ./install.sh [--dry-run] [--claude-only | --codex-only]

  --dry-run      print what would change, change nothing
  --claude-only  link into Claude Code only
  --codex-only   link into Codex only

Targets: $CLAUDE_DIR (default ~/.claude) and $CODEX_DIR (default ~/.codex).
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
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

# Each source as "name<TAB>absolute path". Skills are directories with a
# SKILL.md; agents are single files with the given extension.
skill_sources() {
  local d
  for d in "$REPO"/skills/*/ "$REPO"/vendor/skills/*/; do
    [ -f "$d/SKILL.md" ] && printf '%s\t%s\n' "$(basename "$d")" "${d%/}"
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

# Remove symlinks that no longer lead anywhere, and links into this repo whose
# source was deleted or renamed. A symlink holds no content of its own.
prune() {
  local dir="$1" label="$2" wanted="$3" entry target name
  for entry in "$dir"/* "$dir"/.[!.]*; do
    [ -L "$entry" ] || continue
    name="$(basename "$entry")"
    case $'\n'"$wanted"$'\n' in
      *$'\n'"$name"$'\n'*) continue ;;
    esac
    target="$(readlink "$entry")"
    if [ ! -e "$entry" ]; then
      say "  prune   $label/$name (dangling -> $target)"
    elif [ "${target#"$REPO"/}" != "$target" ]; then
      say "  prune   $label/$name (no longer in the kit)"
    else
      continue
    fi
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

skills="$(skill_sources)"
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
