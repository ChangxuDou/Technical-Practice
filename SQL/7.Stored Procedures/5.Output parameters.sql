-- SELECT
-- CALL → 直接返回/展示结果

-- OUT
-- CALL → 把结果装进 @变量 → SELECT @变量 → 展示结果


DROP PROCEDURE IF EXISTS get_unpaid_invoices;
DELIMITER $$
CREATE PROCEDURE get_unpaid_invoices
(
	client_id INT,
    OUT invoices_total DECIMAL(9,2), 
    OUT invoices_count INT
)
BEGIN
	SELECT SUM(invoice_total) AS total, COUNT(*) AS count
    INTO invoices_total,invoices_count
    FROM invoices i
    WHERE i.client_id = client_id 
    AND payment_total = 0 ;

END $$
DELIMITER ;