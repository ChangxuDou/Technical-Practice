-- use the same table 
-- connect the information with the Manager who the employees report to
-- warning: the Data of manager will lost 

use sql_hr;
SELECT 
	e.employee_id, e.first_name, m.first_name as manager
from employees e
JOIN employees m 
	ON e.reports_to = m.employee_id;

