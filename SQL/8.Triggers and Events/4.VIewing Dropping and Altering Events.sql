SHOW EVENTS;
SHOW EVENTS LIKE'yearly';
DROP EVENT IF EXISTS yearly_delete_stale_audit_rows;
ALTER EVENT... --like CREATE EVENT ,change Schedule directly
ALTER EVENT yearly_delete_stale_audit_rows ENABLE;
