-- update the data of invoices which client_id is 3 and 4
UPDATE invoices
SET 
	payment_total = invoice_total * 0.5,
    payment_date = due_date
WHERE client_id IN (3,4)



-- give any customers born before 1990 ,50extra points

USE sql_store;
UPDATE customers c
SET c.points = points + 50
WHERE birth_date < '1990-01-01'