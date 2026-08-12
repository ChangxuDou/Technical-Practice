-- add a new customer ,who has a new order , which has one product
-- warning: the PK from the Table must be saved and used in next table data inserting

USE store;
INSERT INTO  customers (first_name,last_name,birth_date,phone,address,city,state,points)
VALUE(
	'STEVE',
    'Jobs',
    '1988-08-08',
    '18767854930',
    'jkjdsdi',
    'Los',
    'WA',
    '2500');
SET @customer_id = LAST_INSERT_ID();

INSERT INTO orders(customer_id,order_date,status,comments,shipped_date,shipper_id)
VALUE(
    @customer_id,
    '2018-08-08',
    1,
    'sdjsidj',
    DEFAULT,
    DEFAULT);
SET @order_id = last_insert_id();

INSERT INTO order_items(order_id,product_id,quantity,unit_price)
VALUE(
	@order_id,
    3,
    8,
    8.88);