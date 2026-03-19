#!/usr/bin/env bash
set -euo pipefail

MODEL="${1:-small}"
MODE="${2:-stale}"

EXTRA_ARGS=()
if [[ "$MODE" == "stale" ]]; then
  EXTRA_ARGS+=(--only-stale)
fi

python3 _plugins/transcribe_audio.py \
  --audio-dir assets/audio \
  --out-dir assets/transcripts \
  --model "$MODEL" \
  "${EXTRA_ARGS[@]}"