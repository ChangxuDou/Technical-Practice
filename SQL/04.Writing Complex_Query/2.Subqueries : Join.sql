-- Find customers who have ordered lettuce(id = 3)
-- 	Select customer_id,first_name,last_name

USE sql_invoicing;
SELECT * 
FROM clients
WHERE client_id NOT IN (
	SELECT DISTINCT client_id
    FROM invoices
);

USE sql_invoicing;
SELECT * 
FROM clients
LEFT JOIN invoices
	USING (client_id)
WHERE invoice_id is NULL;


-- EXERCISE--

-- Subqueries --
USE sql_store;
SELECT customer_id, first_name, last_name
FROM customers
WHERE customer_id in (
		SELECT customer_id
        FROM orders
		WHERE order_id in(
				SELECT DISTINCT order_id
				FROM order_items
				WHERE product_id = 3
		)
);

-- JOIN --
USE sql_store;
SELECT c.customer_id, first_name, last_name
	FROM customers c
LEFT JOIN orders o
	ON c.customer_id = o.customer_id
JOIN order_items oi
	USING (order_id)
WHERE product_id = 3
GROUP BY c.customer_id, first_name, last_name