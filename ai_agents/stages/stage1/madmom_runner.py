from __future__ import annotations

from typing import List
import numpy as np
import collections
import collections.abc

# Monkeypatch for madmom compatibility with Python 3.10+ and NumPy 1.20+
if not hasattr(np, "float"):
    np.float = float
if not hasattr(np, "int"):
    np.int = int
collections.MutableSequence = collections.abc.MutableSequence


def extract_beats_onsets(audio_path: str) -> tuple[list[float], list[float]]:
    try:
        import madmom  # type: ignore
        from madmom.features.beats import DBNBeatTrackingProcessor, RNNBeatProcessor  # type: ignore
        from madmom.features.onsets import OnsetPeakPickingProcessor, RNNOnsetProcessor  # type: ignore
    except Exception as e:
        raise ImportError(
            "madmom not installed; install madmom to enable beat/onset extraction"
        ) from e

    proc = DBNBeatTrackingProcessor(fps=100)
    act = RNNBeatProcessor()(audio_path)
    beats = [float(t) for t in proc(act)]

    onset_proc = OnsetPeakPickingProcessor()
    onset_act = RNNOnsetProcessor()(audio_path)
    onsets = [float(t) for t in onset_proc(onset_act)]

    beats = sorted({round(t, 3) for t in beats})
    onsets = sorted({round(t, 3) for t in onsets})
    return beats, onsets
