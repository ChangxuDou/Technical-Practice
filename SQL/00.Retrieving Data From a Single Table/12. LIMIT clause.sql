-- select the customer table
-- limit the items that DB returns
-- skip the first 6 records(offset) to see the next 3 records

-- page 1: 1-3
-- page 2: 4-6
-- page 3: 7-9 (this is wanted)

-- SELECT * 
-- FROM sql_store.customers
-- limit 6,3;

-- get the the top 3 loyal customers(who has the most points)
SELECT * 
FROM sql_store.customers
order by points DESC
limit 3;

