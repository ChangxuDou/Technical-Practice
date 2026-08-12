-- be aware of the implicit syntax,but batter to use explicit syntax

-- SELECT * 
-- FROM sql_store.orders o
-- JOIN customers c
-- 	    ON o.customer_id = c.customer_id;
    
SElECT *
FROM orders o, customers c
WHERE o.customer_id = c.customer_id;
-- in MySQL is this available