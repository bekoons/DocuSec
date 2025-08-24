import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.framework_loader import load_frameworks


def test_load_frameworks_empty_file(tmp_path):
    empty_seed = tmp_path / "seed_frameworks.json"
    empty_seed.write_text("")

    result = load_frameworks(str(empty_seed))

    assert result == {}
