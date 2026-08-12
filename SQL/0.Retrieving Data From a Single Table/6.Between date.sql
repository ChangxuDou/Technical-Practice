-- Return customer born between 01.01.1991 - 01.01.2000


SELECT * 
FROM sql_store.customers
where birth_date BETWEEN '1991-01-01' AND '2000-01-01';
