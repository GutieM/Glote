CREATE TABLE weather_observations (
    id              BIGSERIAL       PRIMARY KEY,
    city_id         BIGINT          NOT NULL REFERENCES cities(id) ON DELETE CASCADE,
    observed_at     TIMESTAMPTZ     NOT NULL,
    fetched_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),
    temperature_c   NUMERIC(4,1),
    humidity_pct    NUMERIC(5,2),
    wind_speed_kmh  NUMERIC(5,2),
    weather_code    INTEGER,
    UNIQUE          (city_id, observed_at)
);