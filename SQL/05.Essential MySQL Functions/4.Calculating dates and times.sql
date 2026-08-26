-- add/subtract a day/month/year,hour/minute/second to the date
SELECT DATE_ADD(NOW(),INTERVAL 1 YEAR) AS NEXT_YEAR;
SELECT DATE_ADD(NOW(),INTERVAL 1 MONTH) AS NEXT_MONTH;
SELECT DATE_ADD(NOW(),INTERVAL 1 DAY) AS NEXT_DAY;
SELECT DATE_ADD(NOW(),INTERVAL 1 HOUR) AS NEXT_HOUR;
SELECT DATE_ADD(NOW(),INTERVAL 1 MINUTE) AS NEXT_MINUTE;
SELECT NOW();
SELECT DATE_SUB(NOW(),INTERVAL 1 YEAR) AS LAST_YEAR;

-- return onle the difference in days
-- DATEDIFF(A, B) = A-B
SELECT DATEDIFF('2019-09-05','2019-04-09');

-- return the number of seconds elapsed since midnight
SELECT time_to_sec('9:00');
SELECT time_to_sec('9:07')- time_to_sec('9:00');