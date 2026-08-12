-- JOIN : combine columns with multiple tables 
-- Warning: the number of columns which is selected must be same with the union data
-- UNION :combine the rows with multiple tables,  comnbine result into one result set


SELECT
	order_id,
    order_date,
    'Active' as status
FROM orders
WHERE order_date >= '2018-01-01'
UNION
SELECT
	order_id,
    order_date,
    'Archive' as status
FROM orders
WHERE order_date < '2018-01-01';


SELECT frirst_name
FROM customers
UNION 
SELECT name
FROM shippers;


-- EXERSISE
SELECT 
	customer_id,first_name,points,'Bronze' as Type
FROM sql_store.customers
WHERE points<2000
UNION 
SELECT 
	customer_id,first_name,points,'Silver' as Type
FROM sql_store.customers
-- WHERE 2000<=points and points <3000 
WHERE points BETWEEN 2000 AND 3000
UNION
SELECT 
	customer_id,first_name,points,'Gold' as Type
FROM sql_store.customers
WHERE points > 3000
ORDER BY first_name;