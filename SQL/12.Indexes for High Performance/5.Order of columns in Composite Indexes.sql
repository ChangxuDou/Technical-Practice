-- Put columns used with equality conditions first
-- Put columns used with range conditions after them
-- For similar conditions, put columns with higher cardinality/selectivity first
-- Consider the other queries the index needs to support
USE sql_store;
EXPLAIN FORMAT = TRADITIONAL
SELECT * FROM sql_store.customers
USE INDEX(idx_lastname_state)
WHERE state = 'CA' AND last_name LIKE 'A%';

CREATE INDEX idx_state_lastname ON customers(state,last_name);-- scan 7 rows

CREATE INDEX idx_lastname_state ON customers(last_name,state);-- scan 40rows