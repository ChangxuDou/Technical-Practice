-- Select clients who have an invooice  -- two Solutions : Subqueries / EXISTS

-- Subqueries: return a result set (list of client_id)  --  shorttage : not efficient if there is a large result
USE sql_invoicing;
SELECT * 
FROM clients
WHERE client_id IN (
	SELECT client_id
    FROM invoices
);

-- EXISTS: WHERE Clause return a boolean to EXISTS operator,then it returns the current record, current client and final result.
USE sql_invoicing;
SELECT *
FROM clients c
WHERE EXISTS(
	SELECT client_id
    FROM invoices
    WHERE client_id = c.client_id
);

-- EXERCISE -- 
-- Find the products that have never been ordered (like Amazon)
USE sql_store;
SELECT * FROM products p
WHERE NOT EXISTS(
	SELECT product_id
    FROM order_items
    WHERE product_id = p.product_id
);

USE sql_store;
SELECT * FROM products
WHERE product_id NOT IN(
	SELECT product_id
    FROM order_items

);