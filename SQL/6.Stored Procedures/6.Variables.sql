-- SQL Server 
-- Connection/Session -- User or session variables
-- Database
-- Table/View/Procedure/Function

-- Funtion / Procedure -- Local Variable 

-- Declare and Use Local Variables in Stored Procedures.
-- Expression: risk_factor = invoices_total / invoices_count * 5

DROP PROCEDURE IF EXISTS get_risk_factor;
DELIMITER $$
CREATE PROCEDURE get_risk_factor()
BEGIN
	DECLARE risk_factor DECIMAL(9,2) DEFAULT 0;
    DECLARE invoices_total DECIMAL(9,2);
	DECLARE invoices_count INT;
    
    SELECT SUM(i.invoice_total),COUNT(*)
    INTO invoices_total,invoices_count
    FROM invoices i ;
    
    SET risk_factor = invoices_total / invoices_count * 5;
    SELECT risk_factor;
    
END $$
DELIMITER ;
