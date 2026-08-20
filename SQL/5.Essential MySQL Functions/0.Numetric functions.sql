-- for more:google'mysql numetric functions'
-- the second parameter is optionnal,specify the precision for rounding
SELECT ROUND(5.7345,3);
SELECT ROUND(5.7345);

-- find the smallsst INT that is bigger than this number (6)
SELECT CEILING(5.2);
-- find the largest INT that is smaller than this number(5)
SELECT FLOOR (5.78);

-- returns the positive value
SELECT ABS(-5.2);

-- generatea a random float pointing number between (0,1)
SELECT RAND();