USE sql_store;
SELECT * FROM sql_store.customers;
SHOW INDEX FROM customers;

CREATE INDEX idx_state_points ON customers(state, points);

EXPLAIN FORMAT = TRADITIONAL
SELECT customer_id FROM customers
WHERE state = 'CA' AND points > 1000; 
-- after we create Composite Indexes,there is 58 rows,previously is 112 rows

DROP INDEX idx_points ON customers;