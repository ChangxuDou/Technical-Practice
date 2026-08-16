-- Select invoices larger than all invoices of 
-- client 3


-- ALL Keyword is the same with MAX Aggrgate operator
-- WARNING: ALL return a list, MAX returns one number

-- MAX aggregate operator--
USE sql_invoicing; 
SELECT * 
FROM invoices
WHERE invoice_total > (
		SELECT MAX(invoice_total)
        FROM invoices
        WHERE client_id = 3
);

-- ALL KEyword-- 
USE sql_invoicing; 
SELECT * 
FROM invoices
WHERE invoice_total > ALL (
		SELECT invoice_total
        FROM invoices
        WHERE client_id = 3
);