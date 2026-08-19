DROP PROCEDURE IF EXISTS get_client_by_state;

DELIMITER $$
CREATE PROCEDURE get_client_by_state
(
	state CHAR(2)
)
BEGIN

SELECT * FROM clients c
WHERE c.state = state;

END $$
DELIMITER  ;

-- EXERCISE --
-- Write a stored procedure to return invoices
-- for a given client(client_id)
-- Procedure name: get_invoices_by_client

DROP PROCEDURE IF EXISTS get_invoice_by_client;

DELIMITER $$
CREATE PROCEDURE get_invoice_by_client
(
	client_id INT
)
BEGIN
	SELECT * FROM invoices i
    WHERE i.client_id = client_id;
END $$

DELIMITER ;