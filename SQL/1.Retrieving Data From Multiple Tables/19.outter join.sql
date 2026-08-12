-- LEFT (outer) join / RIGHT (outer) join
-- it will return all the column from the left table wheather the conditon is true,even if there is null value
-- Join means (inner) join,it will return the columns that all the two tables have


-- SELECT 
-- 	 c.customer_id,c.first_name,c.last_name,o.order_id
-- FROM sql_store.customers c
-- LEFT JOIN orders o
-- 	  ON c.customer_id = o.customer_id
-- ORDER BY c.customer_id;

-- EXERCISE
-- see how many times each product is ordered
-- left Join : return all the data from the left table 
-- warning : order by can influence the results if the columns from the table dont have the total date

SELECT
	order_id,p.product_id,p.name,quantity 
FROM products p
LEFT JOIN order_items oi
	ON oi.product_id = p.product_id
ORDER BY p.product_id;
-- ORDER BY oi.product_id : use this column will lost some result