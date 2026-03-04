from __future__ import annotations

from typing import List

from src.models.stage1 import WhisperSegment


def transcribe(
    audio_path: str,
    model_name: str = "small",
    language: str | None = None,
    initial_prompt: str | None = None,
) -> List[WhisperSegment]:
    try:
        import whisper  # type: ignore
    except Exception as e:
        raise ImportError(
            "whisper not installed; install openai-whisper to enable STT"
        ) from e

    model = whisper.load_model(model_name)
    result = model.transcribe(
        audio_path, language=language, initial_prompt=initial_prompt
    )
    segments = result.get("segments", []) or []
    out: List[WhisperSegment] = []
    for seg in segments:
        start = float(seg.get("start", 0.0))
        end = float(seg.get("end", start))
        text = seg.get("text", "").strip()
        if not text:
            continue
        if end <= start:
            continue
        out.append(WhisperSegment(text=text, start=start, end=end))
    return out
