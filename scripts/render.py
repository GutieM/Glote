import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Paths anchored to repo root (this file lives in scripts/).
ROOT = Path(__file__).resolve().parent.parent
QUERY = ROOT / "db" / "queries" / "latest_per_city.sql"
TEMPLATES = ROOT / "templates"
OUTPUT = ROOT / "docs" / "index.html"


def main():
    load_dotenv()
    sql = QUERY.read_text(encoding="utf-8")

    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql)
            cities = cur.fetchall()

    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(["html"]),
    )
    html = env.get_template("dashboard.html.j2").render(cities=cities)

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Wrote {len(cities)} cities to {OUTPUT}")


if __name__ == "__main__":
    main()