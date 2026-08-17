-- Create a view to see the balance
-- for each client 
-- (view name : client_balance),columns: client_id, name, balance

-- Version 1:NO join
USE sql_invoicing;
CREATE VIEW clients_balance AS 
SELECT 
	c.client_id,name,
    (SELECT SUM(invoice_total - payment_total)
    FROM invoices
    WHERE client_id = c.client_id)AS balance
 FROM clients c;
 
-- Version 2: join
USE sql_invoicing;
CREATE VIEW clients_balance AS 
SELECT 
	c.client_id,
    name, 
    SUM(invoice_total-payment_total) AS balance
 FROM clients c
 LEFT JOIN invoices USING (client_id)
 GROUP BY client_id,name;