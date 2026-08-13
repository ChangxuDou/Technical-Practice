

USE sql_invoicing;

SELECT 
	'FIRST half of 2019' as date_range,
    SUM(invoice_total) AS total_sales,
    SUM(payment_total) AS total_payments,
    SUM(invoice_total- payment_total) AS experct
FROM sql_invoicing.invoices
WHERE invoice_date > '2019-01-01' and invoice_date <'2019-07-01'
UNION
SELECT 
	'SECOND half of 2019' as date_range,
    SUM(invoice_total) AS total_sales,
    SUM(payment_total) AS total_payments,
    SUM(invoice_total- payment_total) AS experct
FROM sql_invoicing.invoices
WHERE invoice_date BETWEEN '2019-07-01' and '2019-12-31'
union
SELECT 
	'Total' as date_range,
    SUM(invoice_total) AS total_sales,
    SUM(payment_total) AS total_payments,
    SUM(invoice_total- payment_total) AS experct
FROM sql_invoicing.invoices
WHERE invoice_date > '2019-01-01' and invoice_date <'2019-12-31'