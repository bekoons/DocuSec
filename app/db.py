import csv
import io
import sqlite3
from typing import Dict, Iterable, List

DB_PATH = "database/frameworks.db"


def _init_db(conn: sqlite3.Connection) -> None:
    """Ensure the frameworks table exists."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS frameworks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            framework_title TEXT NOT NULL,
            control_number TEXT NOT NULL,
            control_language TEXT NOT NULL
        )
        """
    )


def insert_controls(rows: Iterable[Dict[str, str]], db_path: str = DB_PATH) -> int:
    """Insert multiple control rows into the database.

    Args:
        rows: Iterable of dictionaries with framework data.
        db_path: Optional path to the SQLite database file.
    Returns:
        Number of inserted rows.
    """
    rows = list(rows)
    if not rows:
        return 0
    conn = sqlite3.connect(db_path)
    _init_db(conn)
    with conn:
        conn.executemany(
            "INSERT INTO frameworks (framework_title, control_number, control_language) VALUES (?, ?, ?)",
            [
                (
                    row["framework_title"],
                    row["control_number"],
                    row["control_language"],
                )
                for row in rows
            ],
        )
    conn.close()
    return len(rows)


def fetch_controls(db_path: str = DB_PATH) -> List[Dict[str, str]]:
    """Retrieve all stored framework controls."""
    conn = sqlite3.connect(db_path)
    _init_db(conn)
    cursor = conn.execute(
        "SELECT framework_title, control_number, control_language FROM frameworks"
    )
    data = [
        {
            "framework_title": ft,
            "control_number": cn,
            "control_language": cl,
        }
        for ft, cn, cl in cursor.fetchall()
    ]
    conn.close()
    return data


def store_csv_in_db(file_bytes: bytes, db_path: str = DB_PATH) -> int:
    """Parse CSV bytes and store the contents into the database.

    Args:
        file_bytes: Raw CSV file content.
        db_path: Optional path to database file.
    Returns:
        Number of controls stored.
    """
    reader = csv.DictReader(io.StringIO(file_bytes.decode("utf-8")))
    rows: List[Dict[str, str]] = []
    required = {"framework_title", "control_number", "control_language"}
    for row in reader:
        if required.issubset(row.keys()):
            rows.append(
                {
                    "framework_title": row["framework_title"],
                    "control_number": row["control_number"],
                    "control_language": row["control_language"],
                }
            )
    return insert_controls(rows, db_path=db_path)
