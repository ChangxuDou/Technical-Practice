{
	"key":value
}

keys are always strings,surrounded with quotes
Values can be Strings,Numbers,Booleans,Arrays or other objects

-- 1.ADD properties-- first expression 
UPDATE products
SET properties = '{
	"dimensions" : [1,2,3],
    "weight": 10,
    "manufacturer":{"name":"sony"}
}'
WHERE product_id =1;

-- 2.ADD properties-- second expression
UPDATE products
SET properties = JSON_OBJECT(
	'weight',10,
    'dimensions',JSON_ARRAY(1,2,3),
    "manufacturer",JSON_OBJECT('name','sony')
    )
WHERE product_id =1;

-- 3.Select properties

SELECT product_id,JSON_EXTRACT(properties,'$.weight') AS weight
-- SELECT product_id,properties -> '$.weight' AS WEIGHT
FROM sql_store.products
WHERE product_id = 1;

SELECT product_id,properties -> '$.dimensions'-- '$.dimensions[1]'
FROM sql_store.products
WHERE product_id = 1;

SELECT product_id,properties -> '$.manufacturer' -- '$.manufacturer.name' 
FROM sql_store.products
WHERE product_id = 1;

SELECT product_id,properties ->> '$.manufacturer.name'-- another ">"
FROM sql_store.products
WHERE properties ->> '$.manufacturer.name' = 'sony';

-- 4.UPDATE existing properties or add new one
UPDATE products
SET properties = JSON_SET(
	properties,
	'$.weight',20,
    '$.age',10
    )
WHERE product_id =1;

SELECT product_id,properties
FROM products;

-- 5.Remove existing properties
UPDATE products
SET properties = JSON_REMOVE(
	properties,
    '$.age'
    )

