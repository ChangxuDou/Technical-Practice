-- see not only from the order table,
-- but also take other tables: customer information and status information

-- SELECT order_id,order_date,c.first_name,c.last_name,s.name AS status
-- FROM sql_store.orders o
-- JOIN customers c on o.customer_id = c.customer_id 
-- JOIN order_statuses s on o.status = s.order_status_id




-- use the other tables like - clients and payments methods
-- make the main table payments easier to read

SELECT 
	payment_id,
    p.date,
    p.amount,
    c.name,
    invoice_id,
    m.name
FROM sql_invoicing.payments p
JOIN clients c 
	on p.client_id = c.client_id
JOIN payment_methods m 
	on p.payment_method = m.payment_method_id;
