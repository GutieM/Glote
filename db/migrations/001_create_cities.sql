CREATE TABLE cities (
    id          BIGSERIAL       PRIMARY KEY,
    name        TEXT            NOT NULL,
    region      TEXT,
    country     TEXT            NOT NULL,
    latitude    NUMERIC(9,6)    NOT NULL,
    longitude   NUMERIC(9,6)    NOT NULL,
    timezone    TEXT            NOT NULL,
    created_at  TIMESTAMPTZ     NOT NULL DEFAULT now(),
    UNIQUE      (latitude, longitude)
);