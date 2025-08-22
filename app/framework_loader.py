from __future__ import annotations

import json
from pathlib import Path
from typing import List


def load_frameworks() -> List[str]:
    """Load available security frameworks from the bundled database.

    The function attempts to read ``seed_frameworks.json`` from the local
    ``database`` directory and falls back to a small hard-coded list if the
    file is absent or invalid.

    Security considerations
    -----------------------
    * Only files within the expected project directory are accessed, but the
      JSON contents are trusted without validation.  In environments where the
      file may be modified by untrusted parties, validate the schema and
      contents to avoid loading malicious data.
    * No authentication or access checks are performed.  Ensure that the
      database path is not writable by unauthorized users.
    """
    db_path = Path(__file__).resolve().parent.parent / "database" / "seed_frameworks.json"
    if db_path.exists() and db_path.stat().st_size > 0:
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    return ["ISO 27001", "NIST 800-53", "SOC 2"]
