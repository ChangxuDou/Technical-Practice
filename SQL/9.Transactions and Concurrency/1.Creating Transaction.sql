-- CREATE a Transaction
USE sql_store;

START TRANSACTION;
INSERT INTO orders(customer_id,order_date,status)
VALUE(1,NOW(),1);

INSERT INTO order_items
VALUE(LAST_INSERT_ID(),2,8,8);
COMMIT; -- ROLLBACK （Execute Current Statement）