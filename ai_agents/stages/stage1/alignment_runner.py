from __future__ import annotations

import logging
from typing import Iterable, List, Optional, Tuple

from src.models.stage1 import SyllableUnit, WhisperSegment

logger = logging.getLogger(__name__)


def _iter_char_segments(segment: dict) -> Iterable[dict]:
    for key in ("char_segments", "char-segments", "chars"):
        for char_seg in segment.get(key, []) or []:
            yield char_seg
    for word in segment.get("words", []) or []:
        for key in ("char_segments", "char-segments", "chars"):
            for char_seg in word.get(key, []) or []:
                yield char_seg


def _to_segments_and_syllables(
    aligned_segments: list[dict],
) -> Tuple[List[WhisperSegment], List[SyllableUnit]]:
    words: List[WhisperSegment] = []
    syllables: List[SyllableUnit] = []

    for seg in aligned_segments:
        start = float(seg.get("start", 0.0))
        end = float(seg.get("end", start))
        text = (seg.get("text") or "").strip()
        if text and end > start:
            words.append(WhisperSegment(text=text, start=start, end=end))

        for char_seg in _iter_char_segments(seg):
            c_text = (char_seg.get("text") or char_seg.get("char") or "").strip()
            c_start = char_seg.get("start")
            c_end = char_seg.get("end")
            if c_text and c_start is not None and c_end is not None:
                c_start_f = float(c_start)
                c_end_f = float(c_end)
                if c_end_f > c_start_f:
                    syllables.append(
                        SyllableUnit(text=c_text, start=c_start_f, end=c_end_f)
                    )

    return words, syllables


def _transcribe_and_align_on_device(
    audio_path: str,
    model_name: str,
    language: Optional[str],
    device: str,
    initial_prompt: Optional[str] = None,
) -> Tuple[List[WhisperSegment], List[SyllableUnit]]:
    try:
        import whisperx  # type: ignore
    except Exception as e:
        raise ImportError(
            "whisperx not installed; install whisperx to enable alignment"
        ) from e

    audio = whisperx.load_audio(audio_path)
    model = whisperx.load_model(model_name, device)
    transcription = model.transcribe(
        audio, language=language, initial_prompt=initial_prompt
    )

    align_model, metadata = whisperx.load_align_model(
        language_code=transcription.get("language"), device=device
    )
    aligned = whisperx.align(
        transcription.get("segments", []),
        align_model,
        metadata,
        audio,
        device,
        return_char_alignments=True,
    )
    return _to_segments_and_syllables(aligned.get("segments", []) or [])


def transcribe_and_align(
    audio_path: str,
    model_name: str = "small",
    language: Optional[str] = None,
    prefer_gpu: bool = True,
    initial_prompt: Optional[str] = None,
) -> Tuple[List[WhisperSegment], List[SyllableUnit]]:
    try:
        import torch  # type: ignore
    except Exception as e:
        raise ImportError("torch not installed; required for whisperx") from e

    if prefer_gpu and torch.cuda.is_available():
        try:
            return _transcribe_and_align_on_device(
                audio_path,
                model_name,
                language,
                device="cuda",
                initial_prompt=initial_prompt,
            )
        except Exception as e:
            logger.warning("WhisperX GPU path failed, falling back to CPU: %s", e)

    return _transcribe_and_align_on_device(
        audio_path,
        model_name,
        language,
        device="cpu",
        initial_prompt=initial_prompt,
    )
