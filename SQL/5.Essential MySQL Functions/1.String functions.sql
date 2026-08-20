-- for more: search for 'mysql string functions'in google

SELECT length('sky') ;

SELECT UPPER('sky');
SELECT LOWER('SKY');

SELECT LTRIM('  sky');
SELECT RTRIM('SKY   ');
SELECT TRIM('  SKY  ');

-- return a few characters
SELECT LEFT('kindergarden',6);
SELECT RIGHT('kindergarden',6);

-- return a few charactors -- the third argumentis optional
SELECT SUBSTRING('kindergarden',3,5);
SELECT SUBSTRING('kindergarden',3);

-- returns the position of the first occurrence of a character or a sequence of characters
SELECT LOCATE('N','kindergarden');
SELECT LOCATE('der','kindergarden');

SELECT REPLACE('Kindergarten','ten','den');

-- use for concatenating two strings
USE sql_store;
SELECT CONCAT(first_name,'',last_name) AS full_name
FROM customers;
