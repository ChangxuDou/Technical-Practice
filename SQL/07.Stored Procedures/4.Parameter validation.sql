-- create a new procedure to(make payment) update values
-- three parameters:invoice_id,payment_total,payment_date

DROP PROCEDURE IF EXISTS make_payment;

DELIMITER $$
CREATE PROCEDURE make_payment
(
	invoice_id INT,
    payment_total DECIMAL(9,2),
    payment_date DATE
)
BEGIN
	IF payment_total <= 0 THEN
		SIGNAL SQLSTATE'22003'
        SET MESSAGE_TEXT = 'invalid payment amount';
	END IF;
	UPDATE invoices i
    SET 
		i.payment_total = payment_total,
        i.payment_date = payment_date
		WHERE i.invoice_id = invoice_id;

END $$
DELIMITER ;