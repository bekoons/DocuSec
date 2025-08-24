import json
import logging
from pathlib import Path
from typing import Dict, Any


def load_frameworks(path: str = "database/seed_frameworks.json") -> Dict[str, Any]:
    """Load security frameworks from a JSON seed file."""
    file_path = Path(path)
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            logging.warning("Invalid JSON in %s; returning empty dictionary.", file_path)
            return {}

