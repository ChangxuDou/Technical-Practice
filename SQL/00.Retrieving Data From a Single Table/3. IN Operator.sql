-- In Operator

SELECT * 
FROM sql_store.customers
where state in ('VA','GA','FL');
-- where state = 'VA' or state = 'GA' or state = 'FL';
-- where state not in ('VA','GA','FL');