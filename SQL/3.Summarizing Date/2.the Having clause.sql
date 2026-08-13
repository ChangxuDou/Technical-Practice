-- see the total_sales and numbers of invoices,sort by client_id
-- add condition: total_sales>500 and numbers>5

-- warning: use HAVING clause to filter data after Group rows; use WHERE before GROUP rows
-- warning: using HAVING can't reference the column which is not included in select clause, but WHERE can
-- SELECT 中出现的非聚合字段，都明确写入 GROUP BY

USE sql_invoicing;
SELECT
	client_id,
    SUM(invoice_total) AS total_sales,
    COUNT(*) AS numbers_of_invoices
FROM sql_invoicing.invoices
GROUP BY client_id
HAVING total_sales >500 AND numbers_of_invoices > 5

-- Get the customers
--		located in Virginia
--		who have spent more than $100

USE sql_store;
SELECT 
	c.customer_id, c.first_name AS name,c.city,c.state,
    COUNT(DISTINCT o.order_id) as number_of_order,
    SUM(oi.quantity * unit_price) AS total
FROM customers c
LEFT JOIN orders o USING (customer_id)
LEFT JOIN order_items oi USING (order_id)
WHERE state='VA'
GROUP BY c.customer_id,
	c.first_name,
    c.city,
    c.state
HAVING total > 100;  