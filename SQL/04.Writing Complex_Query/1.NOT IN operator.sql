-- Find the products that have never been ordered
USE sql_store;
SELECT * FROM products
WHERE product_id NOT IN(
	SELECT DISTINCT product_id
    FROM order_items
);

-- EXERCISE -- 
-- Find clients without invoices
USE sql_invoicing;
SELECT * 
FROM clients
WHERE client_id NOT IN (
	SELECT DISTINCT client_id
    FROM invoices
);