from __future__ import annotations

import hashlib
import json
import logging
import os
import random
import shutil
import wave
from pathlib import Path
from typing import Dict, Optional

from src.utils.fs import create_run_dirs, get_project_root
from src.models.stage1 import Stage1Output, WhisperSegment, SoundEvent
from .stage1 import alignment_runner, demucs_runner, madmom_runner, whisper_runner

logger = logging.getLogger(__name__)


def _ensure_paths(mode: str, ctx_paths: Optional[Dict[str, str]]) -> Dict[str, str]:
    if ctx_paths:
        return ctx_paths
    _, paths = create_run_dirs(mode)
    _, paths = create_run_dirs(mode)
    return paths


def _read_lyrics(input_file: str) -> Optional[str]:
    """
    Look for a lyrics file (input_file.replace extension with .txt or just lyrics.txt).
    Read and return content for initial_prompt.
    """
    # 1. Try same name as audio but .txt
    p = Path(input_file)
    lyrics_path = p.with_suffix(".txt")
    if not lyrics_path.exists():
        # 2. Try lyrics.txt in same dir
        lyrics_path = p.parent / "lyrics.txt"

    if not lyrics_path.exists():
        return None

    try:
        text = lyrics_path.read_text(encoding="utf-8").strip()
        # Optional: Filter out metadata/timestamps if user pastes raw LRC?
        # For now, just pass the raw text or the first N lines if it's too huge.
        # Check for start/end markers if needed, or just use whole text.
        return text[:1000]  # Limit prompt length to avoid overflow or hallucinations
    except Exception:
        logger.warning("Failed to read lyrics from %s", lyrics_path)
        return None


def _write_silence_wav(path: Path, duration_s: float = 0.1, sr: int = 16000) -> None:
    frames = int(duration_s * sr)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(b"\x00\x00" * frames)


def _mock_run(
    input_file: str, ctx: Dict[str, object], paths: Dict[str, str]
) -> Stage1Output:
    run_id = ctx.get("run_id") or Path(paths["root"]).name
    stage1_dir = Path(paths.get("stage1", Path(paths["final"]) / "stage1_audio"))
    stage1_dir.mkdir(parents=True, exist_ok=True)

    stems: Dict[str, str] = {}
    for stem_name in ["vocals", "drums", "bass", "other"]:
        stem_path = stage1_dir / f"{stem_name}.wav"
        _write_silence_wav(stem_path)
        rel_path = os.path.relpath(stem_path, get_project_root())
        stems[stem_name] = rel_path

    duration_sec = 10.0
    bpm = 120
    beat_interval = 60.0 / bpm
    beats = [round(t, 3) for t in _frange(0.0, duration_sec, beat_interval)]
    onsets = [
        round(t + 0.05 * random.random(), 3) for t in beats if t + 0.2 < duration_sec
    ]

    words = [WhisperSegment(text="demo", start=0.2, end=0.4)]
    sound_events = [
        SoundEvent.model_validate({"time": 1.0, "class": "drum", "confidence": 0.9})
    ]

    return Stage1Output(
        segment_id=str(run_id),
        duration_sec=duration_sec,
        sample_rate=44100,
        stems=stems,
        beats=beats,
        onsets=onsets,
        words=words,
        syllables=[],
        sound_events=sound_events,
    )


def _real_run(
    input_file: str, ctx: Dict[str, object], paths: Dict[str, str]
) -> Stage1Output:
    run_id = ctx.get("run_id") or Path(paths["root"]).name
    stage1_dir = Path(paths.get("stage1", Path(paths["final"]) / "stage1_audio"))
    stage1_dir.mkdir(parents=True, exist_ok=True)

    use_gpu = os.getenv("STAGE1_USE_GPU", "0") == "1"
    use_whisperx = os.getenv("STAGE1_USE_WHISPERX", "0") == "1"
    model_name = os.getenv("WHISPER_MODEL", "small")
    language = os.getenv("WHISPER_LANGUAGE")

    stems_abs = demucs_runner.separate_stems(
        input_file, str(stage1_dir), use_gpu=use_gpu
    )
    beats, onsets = madmom_runner.extract_beats_onsets(input_file)

    initial_prompt = _read_lyrics(input_file)
    if initial_prompt:
        logger.info("Using lyrics as initial_prompt for Whisper")

    words: list[WhisperSegment] = []
    syllables = []

    if use_whisperx:
        try:
            words, syllables = alignment_runner.transcribe_and_align(
                input_file,
                model_name=model_name,
                language=language,
                prefer_gpu=use_gpu,
                initial_prompt=initial_prompt,
            )
        except ImportError as e:
            logger.warning("WhisperX unavailable, falling back to whisper: %s", e)
            if os.getenv("STAGE1_REQUIRE_WHISPERX", "0") == "1":
                raise
        except Exception as e:
            logger.warning("WhisperX alignment failed, falling back to whisper: %s", e)
            if os.getenv("STAGE1_REQUIRE_WHISPERX", "0") == "1":
                raise

    if not words:
        words = whisper_runner.transcribe(
            input_file,
            model_name=model_name,
            language=language,
            initial_prompt=initial_prompt,
        )
        syllables = []

    stems_rel = {
        k: os.path.relpath(v, get_project_root()) for k, v in stems_abs.items()
    }
    sound_events = []

    return Stage1Output(
        segment_id=str(run_id),
        duration_sec=max(onsets[-1] if onsets else 0.0, beats[-1] if beats else 0.0),
        sample_rate=44100,
        stems=stems_rel,
        beats=beats,
        onsets=onsets,
        words=words,
        syllables=syllables,
        sound_events=sound_events,
    )


def _file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_cached(cache_dir: Path) -> Optional[Stage1Output]:
    cache_file = cache_dir / "stage1_output.json"
    if not cache_file.exists():
        return None
    data = json.loads(cache_file.read_text())
    return Stage1Output.model_validate(data)


def _store_cache(cache_dir: Path, output: Stage1Output) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / "stage1_output.json"
    cache_file.write_text(output.model_dump_json(indent=2, ensure_ascii=False))


def _copy_cached_stems_to_run(
    cached: Stage1Output, run_stage1_dir: Path
) -> Dict[str, str]:
    result = {}
    root = Path(get_project_root())
    for stem_name, rel_path in cached.stems.items():
        src = root / rel_path
        dest = run_stage1_dir / Path(rel_path).name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.copy2(src, dest)
        result[stem_name] = os.path.relpath(dest, root)
    return result


def run(input_file: str, ctx: Optional[Dict[str, object]] = None) -> Stage1Output:
    ctx = ctx or {}
    mode = ctx.get("mode", "dev")  # type: ignore[assignment]
    paths = _ensure_paths(mode, ctx.get("paths"))  # type: ignore[arg-type]

    use_real = os.getenv("STAGE1_REAL", "0") == "1"

    cache_dir = (
        Path(get_project_root()) / "data" / "cache" / _file_hash(input_file) / "stage1"
    )
    if use_real:
        cached = _load_cached(cache_dir)
        if cached:
            run_stage1_dir = Path(
                paths.get("stage1", Path(paths["final"]) / "stage1_audio")
            )
            stems = _copy_cached_stems_to_run(cached, run_stage1_dir)
            return cached.model_copy(update={"stems": stems})
        try:
            output = _real_run(input_file, ctx, paths)
            _store_cache(cache_dir, output)
            return output
        except ImportError:
            if os.getenv("STAGE1_REQUIRE_REAL", "0") == "1":
                raise
    return _mock_run(input_file, ctx, paths)


def _frange(start: float, stop: float, step: float):
    t = start
    while t < stop:
        yield t
        t += step
