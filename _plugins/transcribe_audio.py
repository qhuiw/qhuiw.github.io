#!/usr/bin/env python3
"""Generate bilingual (Chinese + English) transcripts for portfolio audio files.

Single file usage:
    python _plugins/transcribe_audio.py \
      --audio assets/audio/your-track.m4a \
      --out assets/transcripts/your-track.json

Batch usage:
    python _plugins/transcribe_audio.py \
      --audio-dir assets/audio \
      --out-dir assets/transcripts \
      --only-stale

Requirements:
  pip install openai-whisper
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import unicodedata
from pathlib import Path


AUDIO_EXTS = {".mp3", ".m4a", ".wav", ".flac", ".ogg", ".aac"}


def compact_segments(segments):
    output = []
    for seg in segments:
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        output.append({"start": int(seg.get("start", 0)), "text": text})
    return output


def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    text = "".join(c if c.isalnum() else "-" for c in text)
    text = "-".join(part for part in text.split("-") if part)
    return text


def build_payload(model, audio_path):
    zh_result = model.transcribe(str(audio_path), language="zh", task="transcribe")
    en_result = model.transcribe(str(audio_path), task="translate")
    return {
        "track": audio_path.stem,
        "source": f"/{audio_path.as_posix().lstrip('./')}",
        "zh": compact_segments(zh_result.get("segments", [])),
        "en": compact_segments(en_result.get("segments", [])),
    }


def _run_whisper_cli(audio_path, model_size, task, language=None):
    whisper_bin = shutil.which("whisper")
    if not whisper_bin:
        raise RuntimeError("whisper CLI not found in PATH")

    with tempfile.TemporaryDirectory(prefix="whisper-out-") as tmp_dir:
        cmd = [
            whisper_bin,
            str(audio_path),
            "--model",
            model_size,
            "--output_format",
            "json",
            "--output_dir",
            tmp_dir,
            "--task",
            task,
        ]
        if language:
            cmd.extend(["--language", language])

        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "whisper CLI failed")

        json_files = sorted(Path(tmp_dir).glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not json_files:
            raise RuntimeError("whisper CLI did not produce json output")

        return json.loads(json_files[0].read_text(encoding="utf-8"))


def build_payload_with_cli(audio_path, model_size):
    zh_result = _run_whisper_cli(audio_path, model_size, task="transcribe", language="zh")
    en_result = _run_whisper_cli(audio_path, model_size, task="translate")
    return {
        "track": audio_path.stem,
        "source": f"/{audio_path.as_posix().lstrip('./')}",
        "zh": compact_segments(zh_result.get("segments", [])),
        "en": compact_segments(en_result.get("segments", [])),
    }


def transcribe_one(model, audio_path, out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_payload(model, audio_path)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Transcript saved to {out_path}")


def transcribe_one_with_cli(model_size, audio_path, out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_payload_with_cli(audio_path, model_size)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Transcript saved to {out_path}")


def find_audio_files(audio_dir):
    return sorted(p for p in audio_dir.rglob("*") if p.suffix.lower() in AUDIO_EXTS)


def resolve_output_name(audio_path, audio_dir, mapping):
    rel_key = audio_path.relative_to(audio_dir).as_posix()
    mapped = mapping.get(rel_key) or mapping.get(audio_path.name)
    if mapped:
        return mapped if mapped.endswith(".json") else f"{mapped}.json"

    slug = slugify(audio_path.stem)
    if not slug:
        slug = f"track-{hashlib.sha1(rel_key.encode('utf-8')).hexdigest()[:8]}"
    return f"{slug}.json"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", help="Path to one audio file")
    parser.add_argument("--out", help="Output JSON path for one audio file")
    parser.add_argument("--audio-dir", help="Directory containing audio files")
    parser.add_argument("--out-dir", help="Directory for transcript JSON files")
    parser.add_argument("--mapping", help="Path to JSON map from audio file to output JSON file")
    parser.add_argument(
        "--model",
        default="small",
        help="Whisper model size (tiny/base/small/medium/large)",
    )
    parser.add_argument(
        "--only-stale",
        action="store_true",
        help="Only refresh transcripts that are missing or older than source audio",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    whisper_backend = "python"
    whisper_model = None
    try:
        import whisper  # type: ignore
    except Exception:
        whisper_backend = "cli"
    else:
        whisper_model = whisper.load_model(args.model)

    mode_single = bool(args.audio or args.out)
    mode_batch = bool(args.audio_dir or args.out_dir)

    if mode_single and mode_batch:
        raise SystemExit("Choose either single-file mode (--audio/--out) or batch mode (--audio-dir/--out-dir).")

    if mode_single:
        if not (args.audio and args.out):
            raise SystemExit("Single-file mode requires both --audio and --out.")

        audio_path = Path(args.audio)
        out_path = Path(args.out)
        if whisper_backend == "python":
            transcribe_one(whisper_model, audio_path, out_path)
        else:
            transcribe_one_with_cli(args.model, audio_path, out_path)
        return

    if mode_batch:
        if not (args.audio_dir and args.out_dir):
            raise SystemExit("Batch mode requires both --audio-dir and --out-dir.")

        audio_dir = Path(args.audio_dir)
        out_dir = Path(args.out_dir)
        mapping = {}

        if args.mapping:
            mapping = json.loads(Path(args.mapping).read_text(encoding="utf-8"))

        files = find_audio_files(audio_dir)
        if not files:
            print("No audio files found.")
            return

        for audio_path in files:
            out_name = resolve_output_name(audio_path, audio_dir, mapping)
            out_path = out_dir / out_name

            if args.only_stale and out_path.exists() and out_path.stat().st_mtime >= audio_path.stat().st_mtime:
                print(f"Skip up-to-date transcript: {out_path}")
                continue

            if whisper_backend == "python":
                transcribe_one(whisper_model, audio_path, out_path)
            else:
                transcribe_one_with_cli(args.model, audio_path, out_path)
        return

    raise SystemExit("Provide either single-file args or batch args.")


if __name__ == "__main__":
    main()
