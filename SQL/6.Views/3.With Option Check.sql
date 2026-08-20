UPDATE  sql_invoicing.invoice_with_balance
SET payment_total = invoice_total
WHERE invoice_id = 4;


-- In VIEW script, add 'WITH CHECK OPTION'
CREATE OR REPLACE VIEW invoice_with_balance AS
SELECT 
	invoice_id,
    number,
    client_id,
    invoice_total-payment_total AS balance,
    invoice_total,
    invoice_date,
    payment_total,
    due_date,
    payment_date
FROM invoices
WHERE (invoice_total-payment_total ) > 0
WITH CHECK OPTION;
