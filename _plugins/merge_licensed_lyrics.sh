#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 4 ]]; then
  echo "Usage: _plugins/merge_licensed_lyrics.sh <transcript.json> <lyrics_zh.txt> <lyrics_en.txt> <output.json> [timeline-from]"
  exit 1
fi

TRANSCRIPT_JSON="$1"
LYRICS_ZH="$2"
LYRICS_EN="$3"
OUTPUT_JSON="$4"
TIMELINE_FROM="${5:-zh}"

python3 _plugins/merge_licensed_lyrics.py \
  --transcript "$TRANSCRIPT_JSON" \
  --lyrics-zh "$LYRICS_ZH" \
  --lyrics-en "$LYRICS_EN" \
  --out "$OUTPUT_JSON" \
  --timeline-from "$TIMELINE_FROM"