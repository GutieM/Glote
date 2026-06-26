# Glote

A small weather dashboard for an international team — built end-to-end to show the engineering
practice behind a data platform.

The two starter cities, Cary, NC and Madrid, Spain; represent a distributed
team across the Americas and Europe. Any team can configure their own list of
locations; adding a city is one config commit.

## v1.0 Scope
- **Cities:** Cary NC, Madrid Spain (configurable; add a city = one config commit)
- **Data:** hourly weather via Open-Meteo
- **Storage:** Supabase Postgres — tables `cities` and `weather_observations`
- **Dashboard:** static HTML, deployed via GitHub Pages
- **Refresh:** scheduled GitHub Actions workflow
- **Quality:** pytest gate on every PR

## Engineering practices demonstrated
- **Atomic commits** — every commit a bounded, reviewable unit
- **Secret hygiene** — `.env.example` as a public contract; `.env` gitignored
- **Smoke testing** — connection verified explicitly before pipeline work
- **Raw SQL migrations** — no ORM; schema is the source of truth
- **Idempotency contracts** — re-running loaders is safe
- **Schema validation** — the pipeline asserts contracts, not just runs

## Roadmap (v1.0)
- [x] Repo init + .gitignore
- [x] Supabase + `.env.example` contract
- [x] Python deps + connection smoke test
- [x] SQL migrations for `cities` + `weather_observations`
- [x] Open-Meteo loader with idempotency
- [x] pytest harness
- [x] GitHub Actions PR gate + scheduled refresh
- [x] Static HTML dashboard + GitHub Pages deploy

## A note on freshness
The dashboard is a **static snapshot**, not a live query — it's only as current as the
last successful refresh. A scheduled GitHub Actions workflow re-runs the pipeline daily
(and on demand) to fetch new observations and republish the page.

The hosted database (Supabase free tier) can pause after inactivity, which freezes the
snapshot until the next run. That's a hosting-cost choice, not an architectural limit: the
pipeline is **database-agnostic** — point `DATABASE_URL` at any Postgres and the loader,
tests, and renderer run unchanged. The tests (hermetic CI container) and the dashboard
(static HTML) never depend on that hosted DB at all.

## v1.1 backlog
- Earthquake fetcher + nearby-city haversine SQL (the original "current affairs" angle)
- Showcase additional cities in the live demo (Seattle, Brazil, England, Poland) — each addition a
one-commit feature demo
- Historical climate extremes via Open-Meteo archive API
- News feed integration
- Mobile-friendly dashboard CSS
- Neon branching for per-PR database isolation
- Dedicated DB roles with least-privilege grants

## Stack
Python · psycopg v3 · Supabase Postgres · GitHub Actions · Jinja2 · raw SQL

## How this was built
This is a portfolio project, openly so. Claude was leveraged to encourage a more industry-standard
flow, to remove any non-industry habits in my workflow I may have picked up from my current
engineering role. The commit history is the evidence — bounded scope per commit, intent in each
message.

I've worked across three versioning eras: Perforce in the enterprise days,
GitHub once it became standard, and now AI-assisted development as the
current shift. The judgment about WHEN to commit, WHAT to bundle, and WHY
a decision was made doesn't get automated.

## Local development
```bash
git clone <repo-url>
cd Glote
python -m venv .venv
.venv\Scripts\activate          # PowerShell on Windows
pip install -r requirements.txt
cp .env.example .env             # then fill in DATABASE_URL
python scripts/test_connection.py