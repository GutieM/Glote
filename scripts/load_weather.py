import os
from datetime import datetime, timezone

import requests
import psycopg
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
CURRENT_FIELDS = "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"

INSERT_SQL = """
    INSERT INTO weather_observations
        (city_id, observed_at, temperature_c, humidity_pct,
        wind_speed_kmh, weather_code)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (city_id, observed_at) DO NOTHING
"""


def main():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, latitude, longitude FROM cities")
            cities = cur.fetchall()

            for city_id, lat, lon in cities:
                params = {
                    "latitude": lat,
                    "longitude": lon,
                    "current": CURRENT_FIELDS,
                }
                resp = requests.get(OPEN_METEO_URL, params=params, timeout=10)
                resp.raise_for_status()
                current = resp.json()["current"]

                observed_at = datetime.fromisoformat(
                    current["time"]
                ).replace(tzinfo=timezone.utc)

                cur.execute(
                    INSERT_SQL,
                    (
                        city_id,
                        observed_at,
                        current["temperature_2m"],
                        current["relative_humidity_2m"],
                        current["wind_speed_10m"],
                        current["weather_code"],
                    ),
                )
                if cur.rowcount:
                    print(f"city {city_id}: stored observation at {observed_at}")
                else:
                    print(f"city {city_id}: already had {observed_at}, skipped")


if __name__ == "__main__":
    main()