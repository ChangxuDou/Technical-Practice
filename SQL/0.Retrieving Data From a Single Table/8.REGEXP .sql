SELECT * 
FROM sql_store.customers
where last_name regexp 'field';

-- where last_name LIKE '%field%'   equals to this sentence

-- where last_name REGEXP '^boa';            ^ means begin with boa
-- WHERE last_name REGEXP 'ey$';             $ means end with ey
-- where last_name REGEXP 'field$|Mac|rose'; | mens or
-- where last_name REGEXP '[gim]e';          []means include 'ge','ie','me'
-- where last_name REGEXP '[a-h]e';          [a-h]e means include ae be ce...