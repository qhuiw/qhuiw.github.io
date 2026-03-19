#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: _plugins/transcribe_audio.sh <audio-file> <output-json> [model]"
  exit 1
fi

AUDIO_FILE="$1"
OUTPUT_JSON="$2"
MODEL="${3:-small}"

python3 _plugins/transcribe_audio.py --audio "$AUDIO_FILE" --out "$OUTPUT_JSON" --model "$MODEL"
