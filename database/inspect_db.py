#!/usr/bin/env python3
"""Inspect the optional SQLite database (non-interactive).

Prints:
- database file path
- tables
- schema for `todos`
- row counts

This is tooling only and not used by the frontend app.
"""

import os
import sqlite3
import sys

DB_NAME = "myapp.db"


def main() -> None:
    """Entry point for DB inspection."""
    if not os.path.exists(DB_NAME):
        print(f"Database file '{DB_NAME}' not found.")
        print("Run: python3 init_db.py")
        sys.exit(1)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys = ON")

        print(f"DB: {os.path.abspath(DB_NAME)}")
        print("")

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
        tables = [r[0] for r in cursor.fetchall()]
        print("Tables:")
        for t in tables:
            print(f"  - {t}")
        if not tables:
            print("  (none)")
        print("")

        if "todos" in tables:
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='todos'")
            row = cursor.fetchone()
            print("Schema: todos")
            print(row[0] if row and row[0] else "(schema not found)")
            print("")

            cursor.execute("SELECT COUNT(*) FROM todos")
            todo_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM todos WHERE completed = 0")
            open_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM todos WHERE completed = 1")
            done_count = cursor.fetchone()[0]

            print("Counts:")
            print(f"  todos.total: {todo_count}")
            print(f"  todos.open:  {open_count}")
            print(f"  todos.done:  {done_count}")
        else:
            print("`todos` table not found. Run: python3 init_db.py")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
