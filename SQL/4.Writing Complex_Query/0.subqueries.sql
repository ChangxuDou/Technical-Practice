-- Find products that are more
-- expensive than Lettuce (id = 3)

USE sql_store;
SELECT * 
FROM sql_store.products
WHERE unit_price > (
	SELECT unit_price
    FROM products
    WHERE product_id = 3);
    
    
-- EXERCISE    
-- In sql_hr database:
-- Find employees whose earn moran than average

USE sql_hr;
SELECT *
FROM employees
WHERE salary >
	(SELECT AVG(salary)
	FROM employees);