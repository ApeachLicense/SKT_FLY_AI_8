from __future__ import annotations

from typing import Dict, Optional, cast

from src.models.stage1 import Stage1Output
from src.models.stage2 import (
    FrameOutput,
    IntentLiteral,
    IntentTag,
    Stage2Output,
    StyleParams,
)
from .stage2_features import compute_intensity_tension
from .stage2_rules import tag_intents


def _style_for(event_type: str, intensity: float, tension: float) -> StyleParams:
    size = 5.0 + 5.0 * intensity
    if event_type == "beat_drop":
        return StyleParams(
            color="#17E5E5",
            font_size_pct=size + 1.0,
            font_weight="bold",
            font_width="expanded",
            animation="pop" if intensity > 0.7 else "pulse",
        )
    if event_type == "vocal_main":
        return StyleParams(
            color="#E5E517",
            font_size_pct=size,
            font_weight="bold",
            font_width="normal",
            animation="word_sync",
        )
    if event_type == "transition":
        return StyleParams(
            color="#E517E5",
            font_size_pct=size,
            font_weight="normal",
            font_width="expanded",
            animation="shake" if tension > 0.5 else "pulse",
        )
    return StyleParams(
        color="#CCCCCC",
        font_size_pct=size,
        font_weight="normal",
        font_width="normal",
        animation="none",
    )


def run(
    stage1_output: Stage1Output, ctx: Optional[Dict[str, object]] = None
) -> Stage2Output:
    times, intensities, tensions = compute_intensity_tension(stage1_output, hop_s=0.5)
    spans = tag_intents(stage1_output, times, intensities, tensions)

    def event_at(t: float) -> IntentLiteral:
        for span in spans:
            if span.start <= t < span.end:
                et = span.event_type
                if et in (
                    "beat_drop",
                    "drum_fill",
                    "vocal_main",
                    "bass_deep",
                    "transition",
                    "beat_anticipation",
                ):
                    return et  # type: ignore[return-value]
        return "beat_anticipation"

    frames = []
    for idx, (t, inten, tens) in enumerate(zip(times, intensities, tensions)):
        etype = cast(IntentLiteral, event_at(t))
        intent = IntentTag(event_type=etype, intensity=inten, harmony_tension=tens)
        style = _style_for(etype, inten, tens)
        frames.append(
            FrameOutput(
                window_idx=idx,
                time_s=t,
                intent_tags=intent,
                style=style,
            )
        )

    return Stage2Output(
        segment_id=stage1_output.segment_id,
        frames=frames,
        dynamics={},
    )
