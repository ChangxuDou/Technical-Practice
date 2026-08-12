-- From the order_item table, get the items
-- for order #6
-- where the total price is greater than 30

use sql_store;
SELECT *
FROM sql_store.order_items
where order_id = 6 and (unit_price * quantity)  > 30 ;