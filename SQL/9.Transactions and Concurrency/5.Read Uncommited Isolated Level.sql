-- First Session
USE sql_store;
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SELECT points
FROM customers
WHERE customer_id = 1;

-- Second Session
USE sql_store;
START TRANSACTION;
UPDATE customers
SET points = 30
WHERE customer_id = 1;
COMMIT;

