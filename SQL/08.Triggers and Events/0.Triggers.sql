-- Test SQL
USE sql_invoicing;
INSERT INTO payments
VALUE(DEFAULT,3,4,'2026-01-01',99,1);

-- Create a Trigger that gets fired when we
-- insert a payment
DROP TRIGGER IF EXISTS payments_after_insert;
DELIMITER $$
CREATE TRIGGER payments_after_insert
	AFTER INSERT ON payments
    FOR EACH ROW
BEGIN
	UPDATE invoices
    SET payment_total = payment_total + NEW.amount
    WHERE invoice_id = NEW.invoice_id;
END $$
DELIMITER ;


-- EXERCISE --
-- Create a Trigger that gets fired when we
-- delete a payment
DROP TRIGGER IF EXISTS payments_after_delete;
DELIMITER $$
CREATE TRIGGER payments_after_delete
	AFTER DELETE ON payments
    FOR EACH ROW
BEGIN 
	UPDATE invoices
    SET payment_total = payment_total - OLD.amount
    WHERE invoice_id = OLD.invoice_id;
END $$
DELIMITER ;

-- Test SQL
USE sql_invoicing;
DELETE FROM payments
WHERE payment_id = 10;