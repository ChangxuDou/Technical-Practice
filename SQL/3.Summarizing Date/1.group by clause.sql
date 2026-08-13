-- use the aggregate function, get the new data and rename as total_sales
-- use group by clause, sort by column: client_id
-- change sort order : use the new column -- total_sales
-- change the range of result : where
USE sql_invoicing;
SELECT
	client_id,
	SUM(invoice_total) AS total_sales
FROM sql_invoicing.invoices 
WHERE invoice_date >= '2019-07-01'
GROUP BY client_id
ORDER BY total_sales DESC;

-- sort by state and city
-- see state,city total_sales

SELECT
	state,
    city,
	SUM(invoice_total) AS total_sales
FROM sql_invoicing.invoices
JOIN clients
	USING(client_id)
GROUP BY state ,city;

-- EXERCISE
-- want the total_payment paid every day with different method

-- get the total_payment
-- sort by each day and payment_method
-- order by date

USE sql_invoicing;
SELECT
	date, 
    m.name as payment_method,
    SUM(p.amount) as total_payments
FROM payments p
JOIN payment_methods m
	ON p.payment_method = m.payment_method_id
GROUP BY date,payment_method
ORDER BY date;