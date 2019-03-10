drop procedure if exists Proc_new_order;

delimiter //


create procedure Proc_new_order(in cur_user_name varchar(20), out cur_ord_id int)
begin
start transaction;
    set cur_ord_id = (select max(order_id)
						from orders);
	if cur_ord_id is null
    then set cur_ord_id = 1;
    end if;
    select cur_ord_id;
    set cur_ord_id = cur_ord_id + 1;
    insert into orders(order_id, user_name, order_time, status)
	values(cur_ord_id, cur_user_name, now(), 'Processing');
commit;
end;
//




delimiter ;
