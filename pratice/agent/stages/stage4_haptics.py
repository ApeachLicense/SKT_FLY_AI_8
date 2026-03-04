from __future__ import annotations

from typing import Dict, Optional

from src.models.stage1 import Stage1Output
from src.models.stage2 import Stage2Output
from src.models.stage3 import Stage3Output
from src.models.stage4 import (
    HapticEvent,
    HapticSignal,
    Stage4Metadata,
    Stage4Output,
    PatternLiteral,
)

FREQ_MAP = {
    "beat_drop": 120,
    "beat_anticipation": 120,
    "drum_fill": 120,
    "bass_deep": 80,
    "vocal_main": 150,
    "transition": 120,
}

PATTERN_MAP: Dict[str, PatternLiteral] = {
    "beat_drop": "pulse_strong",
    "drum_fill": "tremolo",
    "bass_deep": "pulse_long_low",
    "vocal_main": "modulated",
    "transition": "ramp_up",
    "beat_anticipation": "pulse_weak_double",
}


def _default_events(beats: list[float]) -> list[HapticEvent]:
    events: list[HapticEvent] = []
    for b in beats:
        events.append(
            HapticEvent(
                start_ms=int(b * 1000),
                duration_ms=120,
                frequency_hz=120,
                amplitude=0.4,
                pattern="pulse",
            )
        )
    return events


def run(
    stage1_output: Stage1Output,
    stage2_output: Stage2Output,
    stage3_output: Stage3Output,
    ctx: Optional[Dict[str, object]] = None,
) -> Stage4Output:
    haptic_signals: list[HapticSignal] = []
    for idx, frame in enumerate(stage2_output.frames):
        freq = FREQ_MAP.get(frame.intent_tags.event_type, 120)
        pattern = PATTERN_MAP.get(frame.intent_tags.event_type, "pulse")
        if pattern not in PATTERN_MAP.values():
            pattern = "pulse"
        amp = min(1.0, max(0.1, frame.intent_tags.intensity))

        events: list[HapticEvent] = [
            HapticEvent(
                start_ms=int(frame.time_s * 1000),
                duration_ms=200,
                frequency_hz=freq,
                amplitude=amp,
                pattern=pattern,
            )
        ]

        signal = HapticSignal(
            caption_index=min(idx + 1, len(stage3_output.captions)) or 1,
            start=frame.time_s,
            end=frame.time_s + 1.0,
            haptic_sequence=events,
            metadata={"source": frame.intent_tags.event_type},
        )
        haptic_signals.append(signal)

    if not haptic_signals:
        events = _default_events(stage1_output.beats)
        if events:
            haptic_signals.append(
                HapticSignal(
                    caption_index=1,
                    start=events[0].start_ms / 1000.0,
                    end=(events[-1].start_ms + events[-1].duration_ms) / 1000.0,
                    haptic_sequence=events,
                    metadata={"source": "beats"},
                )
            )

    metadata = Stage4Metadata(total_signals=len(haptic_signals))
    return Stage4Output(haptic_signals=haptic_signals, metadata=metadata)
