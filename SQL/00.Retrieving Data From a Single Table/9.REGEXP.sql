# Get the customer whose
# first name are ELKA or AMBUR
# last names end with EY or ON
# last names start with MY or contains SE
# last names contain B followed by R or U

SELECT * 
FROM sql_store.customers
WHERE first_name REGEXP 'ELKA|AMBUR'
-- WHERE first_name LIKE 'ELKA'or first_name LIKE 'AMBUR';

-- WHERE last_name REGEXP 'EY$|ON$';

-- WHERE last_name REGEXP '^my|se';

-- WHERE last_name REGEXP 'B[R|U]';