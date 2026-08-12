-- the USE clause instead of ON 
-- WARNING: the columns name must be the same, the status from order is different from order_status_id

SELECT order_id,c.first_name as customer,sh.name as shipper
FROM sql_store.orders o
LEFT JOIN customers c
	USING (customer_id)
-- 	ON o.customer_id = c.customer_id
LEFT JOIN shippers sh
	USING (shipper_id)
-- 	ON o.shipper_id = sh.shipper_id;


-- compound join condition
SELECT * 
FROM sql_store.order_items oi
JOIN order_item_notes oin
	USING(order_id,product_id);
-- 	 ON oi.order_id = oin.order_id
--   AND oi.product_id = oin.product_id;


-- EXERCISE
-- see the information from payment ,client,payment_method
-- the columns name are not the same (payment_method & payment_method_id)

USE sql_invoicing;
SELECT 
	payment_id,
    p.date,
    c.name AS client,
    p.amount,m.name as method
FROM sql_invoicing.payments p
LEFT JOIN clients c
	USING(client_id)
LEFT JOIN payment_methods m
	on p.payment_id = m.payment_method_id;
