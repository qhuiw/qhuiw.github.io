#!/usr/bin/env python3
"""Merge licensed lyrics into an existing transcript timeline.

This script does NOT crawl or scrape lyrics. It expects licensed lyrics files
provided by the user and aligns them against an existing transcript timeline.

Usage:
  python3 _plugins/merge_licensed_lyrics.py \
    --transcript assets/transcripts/wanwu-buru-ni.json \
    --lyrics-zh path/to/licensed_zh.txt \
    --lyrics-en path/to/licensed_en.txt \
    --out assets/transcripts/wanwu-buru-ni.licensed.json \
    --source-zh-url "https://licensed-provider.example/track" \
    --source-en-url "https://licensed-provider.example/track-en"
"""

from __future__ import annotations

import argparse
import copy
import difflib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript", required=True, help="Input transcript JSON")
    parser.add_argument("--lyrics-zh", help="Licensed Chinese lyrics text file")
    parser.add_argument("--lyrics-en", help="Licensed English lyrics text file")
    parser.add_argument("--out", required=True, help="Output transcript JSON path")
    parser.add_argument(
        "--timeline-from",
        choices=["zh", "en"],
        default="zh",
        help="Timeline source for interpolation when line counts differ",
    )
    parser.add_argument(
        "--en-timeline",
        choices=["zh", "en", "auto"],
        default="zh",
        help="Timeline source for English lyric timing (default zh for translated lyrics)",
    )
    parser.add_argument("--source-zh-url", default="", help="Attribution URL for Chinese lyrics")
    parser.add_argument("--source-en-url", default="", help="Attribution URL for English lyrics")
    parser.add_argument("--source-zh-name", default="", help="Attribution provider name for Chinese lyrics")
    parser.add_argument("--source-en-name", default="", help="Attribution provider name for English lyrics")
    parser.add_argument(
        "--license-note",
        default="Licensed lyrics provided by rights holder/source.",
        help="Compliance note stored in output metadata",
    )
    return parser.parse_args()


def load_text_lines(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    # Keep lyrical line breaks, ignore empty spacer lines.
    return [line.strip() for line in lines if line.strip()]


def ensure_timeline(transcript: dict, language: str) -> list[dict]:
    lines = transcript.get(language) or []
    return [line for line in lines if isinstance(line, dict) and "start" in line]


def interpolate_starts(base_starts: list[float], n: int) -> list[int]:
    if not base_starts:
        return [0] * n
    if n <= 1:
        return [int(round(base_starts[0]))]
    if len(base_starts) == 1:
        return [int(round(base_starts[0])) for _ in range(n)]

    out = []
    max_idx = len(base_starts) - 1
    for i in range(n):
        pos = i * max_idx / (n - 1)
        lo = int(math.floor(pos))
        hi = min(lo + 1, max_idx)
        frac = pos - lo
        start = base_starts[lo] * (1.0 - frac) + base_starts[hi] * frac
        out.append(int(round(start)))

    # Ensure monotonic non-decreasing starts.
    for i in range(1, len(out)):
        if out[i] < out[i - 1]:
            out[i] = out[i - 1]
    return out


def normalize_text(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^\w\u4e00-\u9fff]", "", text)
    return text


def align_starts_by_text(lyrics: list[str], timeline: list[dict], min_score: float = 0.33) -> list[int]:
    if not lyrics:
        return []

    timeline_starts = [float(line.get("start", 0)) for line in timeline]
    baseline = interpolate_starts(timeline_starts, len(lyrics))
    if not timeline:
        return baseline

    n = len(lyrics)
    m = len(timeline)

    lyric_norm = [normalize_text(line) for line in lyrics]
    timeline_norm = [normalize_text(str(line.get("text", ""))) for line in timeline]

    sim = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if lyric_norm[i] and timeline_norm[j]:
                sim[i][j] = difflib.SequenceMatcher(None, lyric_norm[i], timeline_norm[j]).ratio()

    # Monotonic alignment dynamic programming:
    # pick a strictly increasing timeline index sequence maximizing total similarity.
    dp = [[-1e18 for _ in range(m)] for _ in range(n)]
    prev = [[-1 for _ in range(m)] for _ in range(n)]

    for j in range(m):
        dp[0][j] = sim[0][j]

    for i in range(1, n):
        best_score = -1e18
        best_idx = -1
        for j in range(m):
            if dp[i - 1][j] > best_score:
                best_score = dp[i - 1][j]
                best_idx = j

            if best_idx >= 0 and best_idx < j:
                dp[i][j] = best_score + sim[i][j]
                prev[i][j] = best_idx

    end_j = max(range(m), key=lambda j: dp[n - 1][j])
    matches = [-1] * n
    cur_j = end_j
    for i in range(n - 1, -1, -1):
        matches[i] = cur_j
        cur_j = prev[i][cur_j] if i > 0 else -1

    anchored = [None] * n
    for i, j in enumerate(matches):
        score = sim[i][j] if j >= 0 else 0.0
        if j >= 0 and score >= min_score:
            anchored[i] = int(round(timeline_starts[j]))

    starts = [None] * n
    for i, value in enumerate(anchored):
        if value is not None:
            starts[i] = value

    known = [i for i, v in enumerate(starts) if v is not None]
    if not known:
        return baseline

    first = known[0]
    for i in range(0, first):
        delta = baseline[i] - baseline[first]
        starts[i] = max(0, starts[first] + delta)

    last = known[-1]
    for i in range(last + 1, n):
        delta = baseline[i] - baseline[last]
        starts[i] = max(starts[last], starts[last] + delta)

    for a, b in zip(known, known[1:]):
        if b == a + 1:
            continue
        sa = starts[a]
        sb = starts[b]
        span = b - a
        for i in range(a + 1, b):
            t = (i - a) / span
            starts[i] = int(round(sa * (1.0 - t) + sb * t))

    out = [int(starts[0])]
    for i in range(1, n):
        out.append(max(out[-1], int(starts[i])))
    return out


def merge_lyrics(lyrics: list[str], timeline: list[dict]) -> list[dict]:
    if not lyrics:
        return timeline

    new_starts = align_starts_by_text(lyrics, timeline)
    return [{"start": int(s), "text": text} for s, text in zip(new_starts, lyrics)]


def merge_lyrics_with_reference_starts(lyrics: list[str], reference: list[dict]) -> list[dict]:
    if not lyrics:
        return []

    ref_starts = [int(line.get("start", 0)) for line in reference if isinstance(line, dict)]
    if not ref_starts:
        return [{"start": 0, "text": text} for text in lyrics]

    if len(ref_starts) == len(lyrics):
        starts = ref_starts
    else:
        # Fallback for length mismatch: interpolate from Chinese timeline starts.
        starts = interpolate_starts([float(s) for s in ref_starts], len(lyrics))

    return [{"start": int(s), "text": text} for s, text in zip(starts, lyrics)]


def main() -> None:
    args = parse_args()

    transcript_path = Path(args.transcript)
    out_path = Path(args.out)

    payload = json.loads(transcript_path.read_text(encoding="utf-8"))
    out = copy.deepcopy(payload)

    zh_timeline = ensure_timeline(out, "zh")
    en_timeline = ensure_timeline(out, "en")
    base_timeline = zh_timeline if args.timeline_from == "zh" else en_timeline

    if args.lyrics_zh:
        zh_lines = load_text_lines(Path(args.lyrics_zh))
        out["zh"] = merge_lyrics(zh_lines, zh_timeline or base_timeline)

    if args.lyrics_en:
        en_lines = load_text_lines(Path(args.lyrics_en))
        # Prefer exact line-to-line timestamp reuse from merged Chinese lyrics.
        # This keeps bilingual lines perfectly aligned during playback.
        if out.get("zh"):
            out["en"] = merge_lyrics_with_reference_starts(en_lines, out["zh"])
        else:
            if args.en_timeline == "zh":
                en_timeline_ref = zh_timeline or base_timeline
            elif args.en_timeline == "en":
                en_timeline_ref = en_timeline or base_timeline
            else:
                en_timeline_ref = en_timeline if en_timeline else (zh_timeline or base_timeline)
            out["en"] = merge_lyrics(en_lines, en_timeline_ref)

    out["lyrics_compliance"] = {
        "licensed": True,
        "license_note": args.license_note,
        "merged_at": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "zh": {
                "name": args.source_zh_name,
                "url": args.source_zh_url,
            },
            "en": {
                "name": args.source_en_name,
                "url": args.source_en_url,
            },
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Licensed lyrics merged into: {out_path}")


if __name__ == "__main__":
    main()