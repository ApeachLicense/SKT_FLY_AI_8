from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from src.models.stage1 import Stage1Output


@dataclass
class IntentSpan:
    event_type: str
    start: float
    end: float
    intensity: float
    harmony_tension: float


def _merge_spans(spans: List[IntentSpan], min_gap: float = 0.2) -> List[IntentSpan]:
    if not spans:
        return []
    spans = sorted(spans, key=lambda s: s.start)
    merged: List[IntentSpan] = [spans[0]]
    for span in spans[1:]:
        prev = merged[-1]
        if span.start <= prev.end + min_gap and span.event_type == prev.event_type:
            new_end = max(prev.end, span.end)
            merged[-1] = IntentSpan(
                event_type=prev.event_type,
                start=prev.start,
                end=new_end,
                intensity=max(prev.intensity, span.intensity),
                harmony_tension=max(prev.harmony_tension, span.harmony_tension),
            )
        else:
            merged.append(span)
    return merged


def tag_intents(
    stage1: Stage1Output,
    times: List[float],
    intensities: List[float],
    tensions: List[float],
) -> List[IntentSpan]:
    spans: List[IntentSpan] = []
    if not times:
        return spans

    avg_intensity = sum(intensities) / len(intensities) if intensities else 0.0

    for t, inten, tens in zip(times, intensities, tensions):
        beat_near = any(abs(t - b) < 0.25 for b in stage1.beats)
        onset_near = any(abs(t - o) < 0.25 for o in stage1.onsets)
        if inten > max(0.6, avg_intensity + 0.2) and (beat_near or onset_near):
            spans.append(IntentSpan("beat_drop", t, t + 0.5, inten, tens))
            continue

        if "vocals" in stage1.stems and stage1.words:
            spans.append(IntentSpan("vocal_main", t, t + 0.5, inten, tens))
            continue

        if tens > 0.5:
            spans.append(IntentSpan("transition", t, t + 0.5, inten, tens))
            continue

        spans.append(IntentSpan("beat_anticipation", t, t + 0.5, inten, tens))

    return _merge_spans(spans)
