-- get the orders that are not shipped

SELECT * 
FROM sql_store.orders
WHERE shipped_date is NULL or shipper_id is NULL;