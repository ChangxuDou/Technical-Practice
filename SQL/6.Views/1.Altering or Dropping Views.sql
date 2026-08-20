-- 2 ways:DROP.REPLACE
DROP VIEW clients_balance;

-- Add 'OR REPLACE'
USE sql_invoicing;
CREATE OR REPLACE VIEW clients_balance AS 
SELECT 
	c.client_id,
    name, 
    SUM(invoice_total-payment_total) AS balance
 FROM clients c
 LEFT JOIN invoices USING (client_id)
 GROUP BY client_id,name
 ORDER BY client_id DESC;