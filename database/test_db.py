#!/usr/bin/env python3
"""Test SQLite database connection (optional tooling).

This only verifies that:
- the DB file exists
- SQLite can connect
- the expected `todos` table exists

This database is NOT required by the app.
"""

import os
import sqlite3
import sys

DB_NAME = "myapp.db"


def main() -> None:
    """Entry point for connection + schema smoke test."""
    if not os.path.exists(DB_NAME):
        print(f"Database file '{DB_NAME}' not found")
        print("Run: python3 init_db.py")
        sys.exit(1)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()[0]

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='todos' AND name NOT LIKE 'sqlite_%'"
        )
        has_todos = cursor.fetchone() is not None

        conn.close()

        print(f"SQLite version: {version}")
        print(f"Schema check: todos table {'FOUND' if has_todos else 'MISSING'}")

        sys.exit(0 if has_todos else 1)
    except sqlite3.Error as e:
        print(f"Connection failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
