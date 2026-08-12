update orders
set comments = "Gold Customer"
where customer_id in
					(select customer_id
					from customers c
					where c.points >3000);

show warnings;