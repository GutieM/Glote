"""Apply pending SQL migrations to the database.

Reads DATABASE_URL from .env, tracks applied migrations in a
schema_migrations table, and applies any db/migrations/*.sql file
not yet recorded — each in its own transaction.
Run from the Glote root: `python scripts/migrate.py`
"""
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

MIGRATIONS_DIR = Path("db/migrations")


def main() -> None:
    load_dotenv()
    url = os.environ["DATABASE_URL"]

    with psycopg.connect(url, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    filename    TEXT        PRIMARY KEY,
                    applied_at  TIMESTAMPTZ NOT NULL DEFAULT now()
                )
                """
            )
            cur.execute("SELECT filename FROM schema_migrations")
            applied = {row[0] for row in cur.fetchall()}

        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            if path.name in applied:
                print(f"skip    {path.name}")
                continue
            sql = path.read_text(encoding="utf-8-sig")
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(sql)
                    cur.execute(
                        "INSERT INTO schema_migrations (filename) VALUES (%s)",
                        (path.name,),
                    )
            print(f"applied {path.name}")


if __name__ == "__main__":
    main()