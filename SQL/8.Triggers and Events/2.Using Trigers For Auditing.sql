-- 1.INSERT ONE ROW in TABLE A and UPDATE DATA in TABLE B automaticly --
-- plus new table 'audit' to log changes
DROP TRIGGER IF EXISTS payments_after_insert;
DELIMITER $$
CREATE TRIGGER payments_after_insert
	AFTER INSERT ON payments
    FOR EACH ROW
BEGIN
	UPDATE invoices
    SET payment_total = payment_total + NEW.amount
    WHERE invoice_id = NEW.invoice_id;
    
    INSERT INTO payments_audit
    VALUE(NEW.client_id,NEW.date,NEW.amount,'Insert',NOW());
END $$
DELIMITER ;

-- Test SQL --
USE sql_invoicing;
INSERT INTO payments
VALUE(DEFAULT,5,9,DATE(NOW()),5,2);

-- 2.DELETE ONE ROW in TABLE A and UPDATE DATA in TABLE B automaticly --
-- plus new table 'audit' to log changes
DROP TRIGGER IF EXISTS payments_after_delete;
DELIMITER $$
CREATE TRIGGER payments_after_delete
	AFTER DELETE ON payments
    FOR EACH ROW
BEGIN
	UPDATE invoices
    SET payment_total = payment_total - OLD.amount
    WHERE invoice_id = OLD.invoice_id;
    
    INSERT INTO payments_audit
    VALUE(OLD.client_id,OLD.date,OLD.amount,'Delete',NOW());
END $$
DELIMITER ;

-- TEST SQL --
USE sql_invoicing;
DELETE FROM payments
WHERE payment_id = 14;