import os
import time
import uuid
from pathlib import Path
from typing import Dict, Tuple


def get_project_root() -> str:
    """Returns the absolute path to the project root."""
    return str(Path(__file__).parent.parent.parent.absolute())


def _new_run_id() -> str:
    return f"{int(time.time())}-{uuid.uuid4().hex[:8]}"


def create_run_dirs(mode: str) -> Tuple[str, Dict[str, str]]:
    """Create a unique run directory structure under outputs/runs/<run_id>.

    dev: creates intermediate + final directories (stage folders under intermediate)
    deploy: creates final (and logs) only
    """

    run_id = _new_run_id()
    root = Path(get_project_root())
    base_run_dir = root / "outputs" / "runs" / run_id

    paths: Dict[str, str] = {
        "root": str(base_run_dir),
        "logs": str(base_run_dir / "logs"),
        "final": str(base_run_dir / "final"),
    }

    if mode == "dev":
        intermediate_base = base_run_dir / "intermediate"
        paths.update(
            {
                "intermediate": str(intermediate_base),
                "stage1": str(intermediate_base / "stage1_audio"),
                "stage2": str(intermediate_base / "stage2_intent"),
                "stage3": str(intermediate_base / "stage3_sdh"),
                "stage4": str(intermediate_base / "stage4_haptic"),
            }
        )

    for path in paths.values():
        os.makedirs(path, exist_ok=True)

    return run_id, paths
