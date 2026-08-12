-- select the item from order 2
-- order by total_price(new colume) descending

SELECT * , quantity * unit_price as total_price
FROM order_items
WHERE order_id = 2 
order by total_price DESC;