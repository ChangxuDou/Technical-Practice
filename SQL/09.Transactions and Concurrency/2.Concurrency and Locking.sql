-- open two connection
-- copy this script to the other
-- execute this script in first connection line by line, don't commit
-- execute the second script

USE sql_store;
START TRANSACTION;
UPDATE customers
SET points = points +10
WHERE customer_id = 1;
COMMIT;