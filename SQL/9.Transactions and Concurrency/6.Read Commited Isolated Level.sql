-- First Session
USE sql_store;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT points FROM customers WHERE customer_id = 1;
SELECT points FROM customers WHERE customer_id = 1;
COMMIT;

-- Second Session
USE sql_store;
START TRANSACTION;
UPDATE customers
SET points = 20 -- 20/30
WHERE customer_id = 1;
ROLLBACK;

