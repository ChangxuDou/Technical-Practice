insert into orders(customer_id,order_date,status)
values(1,'2020-1-1',2);

insert into order_items(order_id, product_id, quantity, unit_price) 
values
(last_insert_id(),1,10,1.11),
(last_insert_id(),2,20,2.22);
select * from order_items;
