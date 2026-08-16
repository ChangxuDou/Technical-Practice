-- for each employee
--      calculate the avg salary for employee.office
--      return the employee if salsary > avg

USE sql_hr;
SELECT * 
FROM employees e
WHERE salary > (
	SELECT AVG(salary)
    FROM employees
    WHERE e.office_id = office_id
);

-- EXERCISE -- 

-- Get invoices that are larger than the
-- client's average invoice amount
-- for example: i habe 5 invoices,the average of them is 165.find the invoice which is larger than avg
USE sql_invoicing;
SELECT * 
FROM invoices i
WHERE invoice_total > (
	SELECT AVG(invoice_total)
    FROM invoices
    WHERE client_id = i.client_id
);