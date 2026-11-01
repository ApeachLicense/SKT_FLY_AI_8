from __future__ import annotations

from typing import Any, Dict, Optional, cast, Literal

from src.models.stage1 import Stage1Output
from src.models.stage2 import Stage2Output
from src.models.stage3 import CaptionItem, Stage3Metadata, Stage3Output, StyleMeta
from .stage3_provider import get_provider

CAPTION_TPL: Dict[str, str] = {
    "beat_drop": "비트 드롭 ▲▲",
    "vocal_main": "보컬이 중심이에요 ♪",
    "transition": "분위기 전환 ▼",
    "drum_fill": "드럼 필 인! ▲",
    "bass_deep": "저음이 울립니다 ▼",
    "beat_anticipation": "비트가 다가와요 ♪",
}


def _add_lyrics(
    captions: list[CaptionItem], stage1_output: Optional[Stage1Output]
) -> None:
    if not stage1_output:
        return
    for word in stage1_output.words:
        captions.append(
            CaptionItem(
                index=1,
                start=word.start,
                end=word.end,
                text=word.text,
                type="lyrics",
                style=StyleMeta(
                    color="#ffffff",
                    font_size_pct=8.0,
                    font_weight="normal",
                    font_width="normal",
                    animation="word_sync",
                    display_mode="overlay",
                ),
            )
        )


def _fallback_captions(
    stage2_output: Stage2Output, stage1_output: Optional[Stage1Output] = None
) -> Stage3Output:
    captions = []

    # 1. Add music events from Stage 2
    for frame in stage2_output.frames:
        text = CAPTION_TPL.get(
            frame.intent_tags.event_type, f"{frame.intent_tags.event_type} ♪"
        )
        # Avoid clutter: only add non-vocal music events if we have real lyrics
        # or keep vocal_events if we don't have real lyrics
        is_vocal_event = frame.intent_tags.event_type == "vocal_main"
        if stage1_output and is_vocal_event:
            continue

        captions.append(
            CaptionItem(
                index=1,  # Will re-index later
                start=frame.time_s,
                end=frame.time_s + 1.0,
                text=text,
                type="music_event",
                style=StyleMeta(
                    color=frame.style.color,
                    font_size_pct=frame.style.font_size_pct,
                    font_weight=frame.style.font_weight,
                    font_width=frame.style.font_width,
                    animation=frame.style.animation,
                    display_mode="overlay",
                ),
            )
        )

    # 2. Add lyrics from Stage 1 if available
    if stage1_output:
        for word in stage1_output.words:
            captions.append(
                CaptionItem(
                    index=0,
                    start=word.start,
                    end=word.end,
                    text=word.text,
                    type="lyrics",
                    style=StyleMeta(
                        color="#ffffff",
                        font_size_pct=8.0,
                        font_weight="normal",
                        font_width="normal",
                        animation="word_sync",
                        display_mode="overlay",
                    ),
                )
            )

    # 3. Sort and re-index
    captions.sort(key=lambda x: x.start)
    for i, c in enumerate(captions):
        c.index = i + 1

    metadata = Stage3Metadata(caption_count=len(captions))
    return Stage3Output(captions=captions, metadata=metadata)


def _as_float(val: Any, default: float) -> float:
    try:
        return float(val)
    except Exception:
        return default


def run(
    stage2_output: Stage2Output,
    stage1_output: Optional[Stage1Output] = None,
    ctx: Optional[Dict[str, object]] = None,
) -> Stage3Output:
    provider = get_provider()
    try:
        raw = provider.generate(stage2_output)
        captions = []
        allowed_anim: set[Literal["pop", "none", "word_sync", "pulse", "shake"]] = {
            "pop",
            "none",
            "word_sync",
            "pulse",
            "shake",
        }
        allowed_mode: set[Literal["overlay", "inline"]] = {"overlay", "inline"}
        for idx, item in enumerate(raw, start=1):
            if not isinstance(item, dict):
                continue
            start = _as_float(item.get("start", 0.0), 0.0)
            end = _as_float(item.get("end", start + 1.0), start + 1.0)
            text = str(item.get("text", "")).strip()
            if not text or end <= start:
                continue
            style_raw = item.get("style", {})
            style_dict: Dict[str, Any] = (
                style_raw if isinstance(style_raw, dict) else {}
            )
            anim_raw = str(style_dict.get("animation", "none"))
            anim_val = anim_raw if anim_raw in allowed_anim else "none"
            anim: Literal["pop", "none", "word_sync", "pulse", "shake"] = cast(
                Literal["pop", "none", "word_sync", "pulse", "shake"], anim_val
            )
            disp_raw = str(style_dict.get("display_mode", "overlay"))
            disp_val = disp_raw if disp_raw in allowed_mode else "overlay"
            disp: Literal["overlay", "inline"] = cast(
                Literal["overlay", "inline"], disp_val
            )
            captions.append(
                CaptionItem(
                    index=idx,
                    start=start,
                    end=end,
                    text=text,
                    type=str(item.get("type", "music_event")),
                    style=StyleMeta(
                        color=str(style_dict.get("color", "#17E5E5")),
                        font_size_pct=_as_float(
                            style_dict.get("font_size_pct", 8.0), 8.0
                        ),
                        font_weight=str(style_dict.get("font_weight", "normal")),
                        font_width=str(style_dict.get("font_width", "normal")),
                        animation=cast(str, anim),  # type: ignore[arg-type]
                        display_mode=cast(str, disp),  # type: ignore[arg-type]
                    ),
                )
            )

        _add_lyrics(captions, stage1_output)

        if captions:
            captions.sort(key=lambda x: x.start)
            for i, c in enumerate(captions):
                c.index = i + 1
            return Stage3Output(
                captions=captions,
                metadata=Stage3Metadata(caption_count=len(captions)),
            )
    except Exception:
        pass
    return _fallback_captions(stage2_output, stage1_output)
