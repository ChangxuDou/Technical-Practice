-- return products with
-- quantity in stock equal to 49, 38, 72

SELECT * 
FROM sql_store.products
where quantity_in_stock in (49,38,72);