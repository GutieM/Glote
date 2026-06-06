
"""Apply seed data to the database.

Reads DATABASE_URL from .env and runs every db/seeds/*.sql file.
Seeds are data, not schema: they are not tracked in
schema_migrations and stay idempotent via ON CONFLICT.
Run from the Glote root: `python scripts/seed.py`
"""
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

SEEDS_DIR = Path("db/seeds")


def main() -> None:
    load_dotenv()
    url = os.environ["DATABASE_URL"]

    with psycopg.connect(url, autocommit=True) as conn:
        for path in sorted(SEEDS_DIR.glob("*.sql")):
            sql = path.read_text(encoding="utf-8-sig")
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(sql)
            print(f"seeded  {path.name}")


if __name__ == "__main__":
    main()