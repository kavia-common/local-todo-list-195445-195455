# Database (Optional Tooling) — SQLite

This `database/` directory is **optional developer tooling** for inspection/testing only.

The Todo app itself is **local-first** and stores data in the **browser** (e.g., localStorage/IndexedDB).  
**Nothing in the frontend reads/writes this SQLite database.** You can delete this folder and the app will still work.

---

## What’s inside

- `myapp.db` — SQLite database file (created/updated by `init_db.py`)
- `init_db.py` — create/upgrade a minimal schema for optional inspection
- `db_shell.py` — small interactive shell to inspect tables/schema/data
- `inspect_db.py` — quick, non-interactive inspection/report script
- `backup_db.sh` / `restore_db.sh` — basic backup/restore helpers (SQLite copy)

---

## Quick start

From this directory:

```bash
cd database
python3 init_db.py
python3 inspect_db.py
python3 db_shell.py
```

If you have the `sqlite3` CLI installed, you can also run:

```bash
sqlite3 myapp.db ".tables"
sqlite3 myapp.db ".schema todos"
```

---

## Schema

### `todos`

A minimal table intended to mirror typical todo fields for testing/inspection.

| column        | type     | notes |
|--------------|----------|------|
| `id`         | INTEGER  | primary key autoincrement |
| `title`      | TEXT     | required |
| `completed`  | INTEGER  | 0/1, default 0 |
| `created_at` | TEXT     | ISO-8601 timestamp, default current time |
| `updated_at` | TEXT     | ISO-8601 timestamp, default current time |

Indexes:
- `idx_todos_completed` on (`completed`)

---

## Example queries

```sql
SELECT * FROM todos ORDER BY created_at DESC;
SELECT COUNT(*) AS open_count FROM todos WHERE completed = 0;
UPDATE todos SET completed = 1, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE id = 1;
```

---

## Notes

- This database is **not** used by the running web app; it is only for optional tooling.
- The scripts do not require any environment variables.
- If you want to view the DB via the Node viewer in `db_visualizer/`, run `python3 init_db.py` first to refresh `db_visualizer/sqlite.env`.
