EXPECTED = {
    "cities": {"id", "name", "country", "latitude", "longitude"},
    "weather_observations": {
        "id", "city_id", "observed_at", "temperature_c",
        "humidity_pct", "wind_speed_kmh", "weather_code",
    },
}


def test_tables_match_migrations(conn):
    for table, columns in EXPECTED.items():
        with conn.cursor() as cur:
            cur.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name = %s",
                (table,),
            )
            actual = {row[0] for row in cur.fetchall()}
        assert columns <= actual, f"{table} missing {columns - actual}"