-- get the orders placed this year

use sql_store;
SELECT *
FROM orders
where order_date >"2018-01-01"and order_date <"2018-12-31" ;