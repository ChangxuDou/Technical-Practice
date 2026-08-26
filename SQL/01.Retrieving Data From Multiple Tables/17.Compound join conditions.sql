-- in table order_items there is no primary key
--  use two keys to match the other table: order_item_notes
SELECT * 
FROM sql_store.order_items o
JOIN order_item_notes n
	on o.order_id = n.order_Id
    and o.product_id = n.product_id;