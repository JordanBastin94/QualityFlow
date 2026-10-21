CREATE TABLE products (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    reference VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE quality_points (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    name VARCHAR(100) NOT NULL,
    min_value NUMERIC(10, 2) NOT NULL,
    max_value NUMERIC(10, 2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    CHECK (min_value <= max_value)
);

CREATE TABLE quality_checks (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    quality_point_id INTEGER NOT NULL
        REFERENCES quality_points(id),
    measured_value NUMERIC(10, 2) NOT NULL,
    checked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(10) NOT NULL
        CHECK (status IN ('pass', 'fail'))
);

CREATE TABLE quality_alerts (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    quality_check_id INTEGER NOT NULL UNIQUE
        REFERENCES quality_checks(id),
    description TEXT NOT NULL,
    priority VARCHAR(10) NOT NULL
        CHECK (priority IN ('low', 'medium', 'high')),
    status VARCHAR(20) NOT NULL DEFAULT 'open'
        CHECK (status IN ('open', 'in_progress', 'resolved')),
    corrective_action TEXT
);