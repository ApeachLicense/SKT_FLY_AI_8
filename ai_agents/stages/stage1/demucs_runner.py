from __future__ import annotations

from pathlib import Path
from typing import Dict


def separate_stems(
    audio_path: str, output_dir: str, use_gpu: bool = False
) -> Dict[str, str]:
    try:
        from demucs.separate import main as demucs_main  # type: ignore
    except Exception as e:
        raise ImportError(
            "demucs not installed; install demucs to enable stage1 real run"
        ) from e

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd_args = ["--out", str(out_dir), audio_path]
    if use_gpu:
        cmd_args.extend(["-d", "cuda"])

    demucs_main(cmd_args)

    # Demucs output structure can vary (e.g. model_name/track_name/stems.wav)
    # We search recursively for the vocals stem to find the correct directory.
    cand_stems = list(out_dir.rglob("vocals.wav"))
    if not cand_stems:
        raise RuntimeError("demucs produced no stems (vocals.wav not found)")

    # Use the directory containing the vocals stem
    stems_dir = cand_stems[0].parent

    result: Dict[str, str] = {}
    # specific 4-stem models produce 'drums', 'bass', 'other'.
    target_stems = ["vocals", "drums", "bass", "other"]

    for stem_name in target_stems:
        cand = stems_dir / f"{stem_name}.wav"
        if cand.exists():
            result[stem_name] = str(cand)

    if not result:
        raise RuntimeError("demucs produced no stems")
    return result
