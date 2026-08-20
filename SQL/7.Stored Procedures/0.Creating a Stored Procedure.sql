DELIMITER ##

CREATE PROCEDURE get_invoices_with_balance()
BEGIN
SELECT * FROM sql_invoicing.clients_balance;
END##

DELIMITER ;get_invoices_with_balance