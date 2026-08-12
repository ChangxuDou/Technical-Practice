-- use the table order_item from database sql_store 
-- join some columns from another DB sql_inventory
-- attention : when you use the table from another DB ,don't forget add the DB name before the table name

USE sql_store;
SELECT *
FROM order_items oi
JOIN sql_inventory.products p ON p.product_id = oi.product_id;