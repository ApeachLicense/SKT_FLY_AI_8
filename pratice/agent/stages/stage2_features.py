from __future__ import annotations

import math
from typing import List, Tuple

from src.models.stage1 import Stage1Output


def compute_intensity_tension(
    stage1: Stage1Output, hop_s: float = 0.5
) -> Tuple[List[float], List[float], List[float]]:
    duration = max(stage1.duration_sec, 0.0)
    frames = max(1, math.ceil(duration / hop_s))
    times = [round(i * hop_s, 3) for i in range(frames)]

    intensities: List[float] = []
    for t in times:
        window_start = t
        window_end = t + hop_s
        count = sum(1 for o in stage1.onsets if window_start <= o < window_end)
        val = min(1.0, count / 3.0)
        intensities.append(val)

    tension_value = 0.0
    if len(stage1.beats) >= 2:
        intervals = [b - a for a, b in zip(stage1.beats, stage1.beats[1:]) if b > a]
        if intervals:
            mean_int = sum(intervals) / len(intervals)
            variance = sum((x - mean_int) ** 2 for x in intervals) / len(intervals)
            std = math.sqrt(variance)
            max_int = max(intervals)
            if max_int > 0:
                tension_value = min(1.0, std / max_int)
    tensions = [tension_value for _ in times]

    return times, intensities, tensions
