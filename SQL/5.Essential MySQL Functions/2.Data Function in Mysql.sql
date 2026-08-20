-- call the NOW function to get the current date and time
SELECT NOW();
-- return current date wothout the time coponent
SELECT CURDATE();
-- return current time without date component
SELECT CURTIME();
-- RETURN INT
SELECT YEAR(NOW());
SELECT MONTH(NOW());
SELECT DAY(NOW());
-- RETURN INT
SELECT HOUR(NOW()),MiNUTE(NOW()),SECOND(NOW());

-- Return String
SELECT DAYNAME(NOW());
SELECT MONTHNAME(NOW());

-- Standard SQL language : more portable (be able to port code to other system)
SELECT extract(YEAR FROM NOW());

-- EXERCISE--
-- RETURN the orders in the current year
SELECT * FROM orders
WHERE YEAR(order_date) >= extract(YEAR FROM NOW());


