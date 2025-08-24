import sys
from pathlib import Path

# Ensure application modules are importable
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.db import fetch_controls, store_csv_in_db


def test_store_csv_and_fetch(tmp_path):
    csv_content = (
        "framework_title,control_number,control_language\n"
        "ISO,1,Policy statement\n"
        "ISO,2,Another control\n"
    )
    db_path = tmp_path / "frameworks.db"
    inserted = store_csv_in_db(csv_content.encode("utf-8"), db_path=str(db_path))
    assert inserted == 2
    data = fetch_controls(db_path=str(db_path))
    assert data == [
        {
            "framework_title": "ISO",
            "control_number": "1",
            "control_language": "Policy statement",
        },
        {
            "framework_title": "ISO",
            "control_number": "2",
            "control_language": "Another control",
        },
    ]
