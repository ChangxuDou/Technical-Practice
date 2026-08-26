-- Subqueried in Select clause
-- invoice_id, invoice_total, invoice_average, difference
USE sql_invoicing;
SELECT invoice_id,invoice_total,
	(SELECT AVG(invoice_total)
    FROM invoices) as average,
    invoice_total - (SELECT average)
FROM invoices;

-- EXERCISE--
-- get: client_id, name, total_sales(all the invoices issued for each client), average (avg of all invoices), difference)
USE sql_invoicing;
SELECT
	DISTINCT c.client_id,
    c.name,
    (SELECT SUM(invoice_total)
		FROM invoices
		WHERE client_id = c.client_id) as total_sales,
    (SELECT AVG(invoice_total)
		FROM invoices) as average,
		(SELECT total_sales - average)
FROM invoices i
RIGHT JOIN clients c
	USING(client_id);

-- standard answer    
USE sql_invoicing;
SELECT 
	client_id,
	name,
    (SELECT SUM(invoice_total)
		FROM invoices
		WHERE client_id = c.client_id) as total_sales,
    (SELECT AVG(invoice_total)
		FROM invoices) as average,
    (SELECT total_sales - average) as difference
FROM clients c;
