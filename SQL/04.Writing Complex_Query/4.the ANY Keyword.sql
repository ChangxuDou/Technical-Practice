-- Select clients with at least two invoices
-- ANY Keyword is like IN

USE sql_invoicing;
SELECT *
FROM clients
WHERE client_id = ANY(
-- WHERE client_id IN (
	SELECT client_id
    FROM invoices
    GROUP BY client_id
    HAVING COUNT(*) >= 2
);