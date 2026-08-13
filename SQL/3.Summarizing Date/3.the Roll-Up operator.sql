USE sql_invoicing;
SELECT 
	pm.name AS payment_method,
    SUM(p.amount) AS total
FROM sql_invoicing.payments p
Join payment_methods pm 
	ON p.payment_method = pm.payment_method_id
GROUP BY pm.name with ROLLUP;
-- Wrong: GROUP BY payment_method with ROLLUP; 
-- WARNING: wen we use ROLLUP operator, we can't use a column alias in GROUP BY clause