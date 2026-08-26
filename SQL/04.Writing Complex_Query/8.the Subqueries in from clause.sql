USE sql_invoicing;
SELECT * 
FROM(
SELECT 
	client_id,
	name,
    (SELECT SUM(invoice_total)
		FROM invoices
		WHERE client_id = c.client_id) as total_sales,
    (SELECT AVG(invoice_total)
		FROM invoices) as average,
    (SELECT total_sales - average) as difference
FROM clients c
)