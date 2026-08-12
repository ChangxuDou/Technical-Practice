

SELECT * 
FROM sql_store.customers
where last_name LIKE 'B%';
-- where last_name LIKE '%B%' (b in the middle/beginning/end, % any number charactors)
-- where last_name LIKE '_y'( _ means single character )
-- where last_name LIKE '_____y'
-- where last_name LIKE 'b____y'