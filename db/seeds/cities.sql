INSERT INTO cities (name, region, country, latitude, longitude, timezone) VALUES
    ('Cary',   'NC', 'United States', 35.791540, -78.781117, 'America/New_York'),
    ('Madrid', NULL, 'Spain',         40.416775,  -3.703790, 'Europe/Madrid')
ON CONFLICT (latitude, longitude) DO NOTHING;