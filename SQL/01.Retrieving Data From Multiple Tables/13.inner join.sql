-- select the columns from table orders
-- join some customer information from table customer 
-- use the same key : customer_id
-- simply the column name: order - o, based on from and join clause
-- attention: the same column must have the table name

-- SELECT first_name, last_name, o.customer_id,order_id
-- FROM sql_store.orders o
-- JOIN  customers c on o.customer_id = c.customer_id;

-- based on the table order_items add the name of the product from the table product
SELECT order_id,p.product_id,name,quantity,oi.unit_price
FROM sql_store.order_items oi
JOIN products p on p.product_id = oi.product_id;