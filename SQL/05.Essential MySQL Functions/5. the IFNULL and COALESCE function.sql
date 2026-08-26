-- IFNULL: if shipper_id is null, return the String 'not assigned'
-- COALESCE : if shipper_id is null, return the value of comments colmumn, if it is also null, return'not assigned'

USE sql_store;
SELECT 
	order_id,
    IFNULL(shipped_date,'not assigned'),
    COALESCE(shipper_id,comments,'not assigned')
FROM orders;