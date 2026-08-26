-- if(expression,first,second)

USE sql_store;
SELECT 
	order_id,
	customer_id,
    order_date,
	shipper_id,
    shipped_date,
    IF(
    YEAR(order_Date) = YEAR(now()),
    'active','archived') AS category
FROM orders;

-- EXERCISE--
USE sql_store;
SELECT 
	product_id,
    name,
    COUNT(*) AS orders,
    IF (COUNT(*) > 1,'many times','once' ) AS frequence
FROM products p
JOIN order_items oi 
	USING(product_id)
GROUP BY product_id, name;
