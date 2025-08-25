import sys
from pathlib import Path
import pytest

# ensure import path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.validation import validate_input
from app.db import store_csv_in_db


def test_validate_input_rejects_sql():
    with pytest.raises(ValueError):
        validate_input("DROP TABLE users;")


def test_validate_input_rejects_script_tag():
    with pytest.raises(ValueError):
        validate_input("<script>alert('x')</script>")


def test_store_csv_rejects_malicious(tmp_path):
    csv_content = (
        "framework_title,control_number,control_language\n"
        "ISO,1,<script>alert(1)</script>\n"
    )
    db_path = tmp_path / "frameworks.db"
    with pytest.raises(ValueError):
        store_csv_in_db(csv_content.encode("utf-8"), db_path=str(db_path))
