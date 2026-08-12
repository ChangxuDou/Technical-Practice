-- we get all the customer who has the order or not
-- we get all the orders who has the shipper or not

-- SELECT 
-- 	c.customer_id,c.first_name,o.order_id,sh.name as shipper
-- FROM sql_store.customers c
-- LEFT JOIN orders o
-- 	ON c.customer_id = o.customer_id
-- LEFT JOIN shippers sh
-- 	ON o.shipper_id = sh.shipper_id;
    
-- EXERCISE
-- see every order detail,weather there is a shipper or not,status is finished or not

SELECT order_id,c.first_name,sh.name as shipper, os.name
FROM sql_store.orders o
LEFT JOIN customers c
	ON o.customer_id = c.customer_id
LEFT JOIN shippers sh
	on sh.shipper_id = o.shipper_id
Left JOIN order_statuses os
	on os.order_status_id = o.status
ORDER BY os.order_status_id;