-- Adaptable Views: If there are no these Keywords or Clause in Views,that means adaptable Views(Insert, Update, Delete)

-- DISTINCT
-- Aggregate Functions (MIN, MAX, SUM, AVG,)
-- GROUP BY / HAVING
-- UNION
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
WHERE (invoice_total-payment_total ) > 0;

-- Delete
DELETE FROM invoice_with_balance
WHERE invoice_id = 1;

-- Update
UPDATE invoice_with_balance
SET due_date = DATE_ADD(due_date,INTERVAL 2 DAY)
WHERE invoice_id = 2;

-- Insert
-- WARNING: we can also insert a new invoice through this view,
-- this only work if the viwa hat all the required columns in the underlying table