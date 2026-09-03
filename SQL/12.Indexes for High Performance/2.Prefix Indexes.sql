-- For STRING, prefix indexes would be better.
USE sql_store;
CREATE INDEX idx_lastname ON customers(last_name(20));
SELECT
	COUNT(DISTINCT LEFT(last_name, 1)),
    COUNT(DISTINCT LEFT(last_name, 5)),
    COUNT(DISTINCT LEFT(last_name, 10))
FROM customers;