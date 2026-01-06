#!/usr/bin/env python3
"""Initialize/upgrade the optional SQLite database schema.

This database is OPTIONAL tooling only and is NOT used by the frontend app.
It exists for developers to inspect/test a minimal schema locally.

Running this script is idempotent: it creates tables if missing.
"""

import os
import sqlite3
from typing import Tuple

DB_NAME = "myapp.db"


def _connect(db_name: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """Create a SQLite connection with sensible defaults."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    # Improves concurrent reads during inspection.
    cursor.execute("PRAGMA journal_mode = WAL")
    return conn, cursor


def _create_schema(cursor: sqlite3.Cursor) -> None:
    """Create the minimal schema used for optional inspection/testing."""
    # Minimal todos table (intentionally not coupled to frontend code).
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0 CHECK (completed IN (0, 1)),
            created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
            updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        )
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_todos_completed
        ON todos(completed)
        """
    )


def _write_connection_info(db_name: str) -> None:
    """Write db_connection.txt with helpful paths/strings for humans/tools."""
    current_dir = os.getcwd()
    connection_string = f"sqlite:///{current_dir}/{db_name}"

    with open("db_connection.txt", "w", encoding="utf-8") as f:
        f.write("# SQLite connection methods:\n")
        f.write(f"# Python: sqlite3.connect('{db_name}')\n")
        f.write(f"# Connection string: {connection_string}\n")
        f.write(f"# File path: {current_dir}/{db_name}\n")


def _write_visualizer_env(db_name: str) -> None:
    """Write env file used by the optional Node.js db_visualizer tool."""
    db_path = os.path.abspath(db_name)

    if not os.path.exists("db_visualizer"):
        os.makedirs("db_visualizer", exist_ok=True)

    with open("db_visualizer/sqlite.env", "w", encoding="utf-8") as f:
        f.write(f'export SQLITE_DB="{db_path}"\n')


def main() -> None:
    """Create/upgrade the SQLite database and write helper metadata files."""
    print("Starting SQLite setup (optional tooling)...")

    db_exists = os.path.exists(DB_NAME)
    if db_exists:
        print(f"SQLite database already exists at {DB_NAME} (will ensure schema is up to date)")
    else:
        print("Creating new SQLite database...")

    conn, cursor = _connect(DB_NAME)
    try:
        _create_schema(cursor)
        conn.commit()

        # Stats
        cursor.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        table_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM todos")
        todo_count = cursor.fetchone()[0]
    finally:
        conn.close()

    # Helper files for humans/tools
    _write_connection_info(DB_NAME)
    _write_visualizer_env(DB_NAME)

    current_dir = os.getcwd()
    print("\nSQLite setup complete!")
    print(f"Database: {DB_NAME}")
    print(f"Location: {current_dir}/{DB_NAME}")
    print("")
    print("Schema:")
    print("  - todos")
    print("")
    print("Database statistics:")
    print(f"  Tables: {table_count}")
    print(f"  Todos:  {todo_count}")
    print("")
    print("Inspect:")
    print("  python3 inspect_db.py")
    print("  python3 db_shell.py")
    print("")
    print("Optional Node viewer:")
    print("  source db_visualizer/sqlite.env")
    print("  cd db_visualizer && npm install && npm start")
    print("")
    print("Script completed successfully.")


if __name__ == "__main__":
    main()
