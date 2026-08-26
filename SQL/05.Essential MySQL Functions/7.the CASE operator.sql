-- CASE expression THEN result

USE sql_store;
SELECT 
	order_id,
    CASE
		WHEN YEAR(order_date) = YEAR(now()) THEN 'Active'
		WHEN YEAR(order_date) = YEAR(now())-1 THEN 'Last year'
		WHEN YEAR(order_date) < YEAR(now())-1 THEN 'Archived'
		ELSE 'Future'
    END AS category
FROM orders;

-- Tipps: the same
SELECT YEAR(DATE_SUB((now()), INTERVAL 1 YEAR));
SELECT YEAR(NOW())-1;


-- EXERCISE -- 
SELECT 
	customer_id,
    concat(first_name,' ',last_name) AS name,
    points,
    CASE
		WHEN points > 3000 THEN 'Gold'
        WHEN points >=2000 THEN 'Silver'
        ELSE 'Bronze'
	END AS category
FROM customers;