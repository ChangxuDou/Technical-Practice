-- cross jion : create test data or create department table
USE sql_store;
SELECT * 
FROM shippers, products;

-- explicit syntax
select *
FROM shippers
CROSS JOIN products;