EXPLAIN FORMAT=TRADITIONAL
SELECT customer_id
FROM customers
WHERE state = 'VA';

create INDEX idx_state ON customers(state);

-- EXERCISE --
-- Write a query to find customers with more than 1000 points;
EXPLAIN FORMAT = TRADITIONAL
SELECT * FROM customers WHERE points > 1000;

CREATE INDEX idx_points ON customers(points);

