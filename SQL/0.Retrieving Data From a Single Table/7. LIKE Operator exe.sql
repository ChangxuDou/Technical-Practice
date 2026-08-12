-- Get the customers whose
-- addresses contain TRAIL or AVENUE
-- phone numbers end with 6

SELECT * 
FROM sql_store.customers
where (address LIKE '%TRAIL%' 
or address LIKE '%AVENUE%')
and phone LIKE'%6';

-- phone numbers not end with 6 
-- phone NOT LIKE '%6'