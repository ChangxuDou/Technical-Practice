-- 1.Copy the table from order ,named order_archive
-- warning: no Primary Key,not marked as auto increment column

CREATE TABLE order _archive AS
SELECT * FROM orders;

-- 2.truncate table :order_archive

-- 3.Insert new rows which is satisfied with some conditions
INSERT INTO order_archive
SELECT * FROM orders
where order_date < '2018-08-08';
-- conclusion: Get the subset from  the original table


-- EXERCISE --
-- get the new table copied from the table invoices , named as invoicing_archive
-- join the information from the table: clients ,such as name
-- invoice with payment date is available
-- warning: no PK,not maked as increment column

USE sql_invoicing;
CREATE TABLE invoicing_archive as
SELECT 
	i.invoice_id,
    i.number,
    c.name as client,
    i.invoice_date,
    i.invoice_total,
    i.payment_date
FROM sql_invoicing.invoices i
LEFT JOIN clients c
	USING(client_id)
WHERE payment_date is NOT NULL;


