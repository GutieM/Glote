"""Smoke-test the Supabase connection.

Reads DATABASE_URL from .env, opens a psycopg v3 connection through
the Supabase Transaction Pooler, and confirms the server responds.
Run from the Glote root: `python scripts/test_connection.py`
"""
import os
import psycopg
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    url = os.environ["DATABASE_URL"]
    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            (version,) = cur.fetchone()
            print(f"Connected. Server says: {version}")


if __name__ == "__main__":
    main()