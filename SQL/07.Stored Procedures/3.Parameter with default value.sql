DROP PROCEDURE IF EXISTS get_client_by_state;

DELIMITER $$
CREATE PROCEDURE get_client_by_state
(
	state CHAR(2)
)
BEGIN
	IF state IS NULL THEN
		SELECT * FROM clients;
    ELSE
		SELECT * FROM clients c
		WHERE c.state = state;
    END IF;
END $$
DELIMITER ;

-- Simplify
DROP PROCEDURE IF EXISTS get_client_by_state;

DELIMITER $$
CREATE PROCEDURE get_client_by_state
(
	state CHAR(2)
)
BEGIN
	SELECT * FROM clients c
	WHERE c.state = IFNULL(state, c.state);
END $$
DELIMITER ;

-- EXERCISE --
-- Write a stored procedure called get_payments
-- with two parameters
-- client_id => INT (4) / payment_method_id=>TINYINT (1) 0-256
-- both parameters are optional.If we pass null of both,return all.If we supply client_id,return only payments for shis client.

DROP PROCEDURE IF EXISTS get_payments;

DELIMITER $$
CREATE PROCEDURE get_payments
(
	client_id INT,
    payment_method_id TINYINT
)
BEGIN
	SELECT * FROM payments p
    WHERE p.client_id = IFNULL(client_id, p.client_id)
    AND p.payment_method = IFNULL(payment_method_id, p.payment_method);
END $$
DELIMITER ;