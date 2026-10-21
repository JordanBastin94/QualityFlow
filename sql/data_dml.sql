-- 1. Create a product
INSERT INTO products (reference, name, description)
VALUES (
    'PROD-001',
    'Metal Component',
    'Metal component subject to dimensional quality checks'
);

-- 2. Create two quality points for this product
INSERT INTO quality_points (
    product_id, name, min_value, max_value, unit
)
VALUES
    (1, 'Length', 9.80, 10.20, 'mm'),
    (1, 'Weight', 95.00, 105.00, 'g');
	