SELECT DISTINCT ON (c.id)
    c.name,
    c.country,
    w.observed_at,
    w.temperature_c,
    w.humidity_pct,
    w.wind_speed_kmh,
    w.weather_code
FROM weather_observations AS w
JOIN cities AS c ON c.id = w.city_id
ORDER BY c.id, w.observed_at DESC;