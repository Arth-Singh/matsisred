#!/usr/bin/env bash
# Smoke-test item prompts through Codex headless (user config model gpt-6-astra).
# Usage: tests/run_codex.sh questions/batch1 [n_samples]
# Output: tests/results/codex_<batch>_<timestamp>/<item>_s<k>.md
set -euo pipefail

ITEMS_DIR="$1"
N="${2:-1}"
HERE="$(cd "$(dirname "$0")" && pwd)"
BATCH="$(basename "$ITEMS_DIR")"
OUT="$HERE/results/codex_${BATCH}_$(date +%Y%m%d_%H%M%S)"
SANDBOX_DIR="$HERE/smoke"
mkdir -p "$OUT" "$SANDBOX_DIR"

PREFIX='You are answering a reasoning question. Do not run commands, read files, or use any tools. Reply with your answer only.

'

for f in "$ITEMS_DIR"/*.md; do
  case "$(basename "$f")" in FORMAT.md|README.md) continue ;; esac
  id="$(basename "$f" .md)"
  prompt="$(python3 - "$f" <<'PY'
import re, sys, pathlib
t = pathlib.Path(sys.argv[1]).read_text()
m = re.search(r"^## Prompt\n(.*?)(?=^## |\Z)", t, re.S | re.M)
if not m or not m.group(1).strip():
    sys.exit("missing prompt in " + sys.argv[1])
print(m.group(1).strip())
PY
)"
  for k in $(seq 0 $((N-1))); do
    out="$OUT/${id}_s${k}.md"
    t0=$(date +%s)
    printf '%s%s' "$PREFIX" "$prompt" | codex exec --skip-git-repo-check --ephemeral -s read-only \
      -C "$SANDBOX_DIR" --color never -o "$out" - >/dev/null 2>"$OUT/${id}_s${k}.stderr" || true
    t1=$(date +%s)
    if [ -s "$out" ]; then
      echo "  ok  $id #$k ($((t1-t0))s)"
    else
      echo "  ERR $id #$k (see $OUT/${id}_s${k}.stderr)"
    fi
  done
done
echo "done -> $OUT"
