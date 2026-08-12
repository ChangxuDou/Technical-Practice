-- select the customer 
-- 1000 <= points <= 3000
-- Between Operator

SELECT * 
FROM sql_store.customers
where points between 1000 and 3000;
-- where points >= 1000 AND points <= 3000;