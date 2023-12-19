CREATE TABLE Observation (
    observation_id SERIAL PRIMARY KEY,
    actual_datetime TIMESTAMP WITHOUT TIME ZONE,
    observation_temp DECIMAL NOT NULL,
    row_date DATE NOT NULL,
    is_day BOOLEAN NOT NULL
);