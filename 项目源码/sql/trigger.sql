delimiter //

drop trigger if exists Tri_flights_airport_insert;
drop trigger if exists Tri_flights_airport_update;
drop trigger if exists Tri_airports_delete;
drop trigger if exists Tri_tickets_delete;
drop trigger if exists Tri_tickets_insert;

create trigger Tri_flights_airport_insert before insert on flights
for each row
begin
    if new.departure_id not in (select airport_id
								from airports)
	then
		signal sqlstate '88888' set message_text = 'Invalid departure airport';
	end if;
	if new.destination_id not in (select airport_id
								  from airports)
	then
		signal sqlstate '88889' set message_text = 'Invalid destination airport';
	end if;
    
    select first_total, business_total, economy_total into @f, @b, @e
    from models
    where new.model_id = models.model_id;
    
    set new.first_left = @f;
    set new.business_left = @b;
    set new.economy_left = @e;
end;
//


create trigger Tri_flights_airport_update before update on flights
for each row
begin
    if new.departure_id not in (select airport_id
								from airports)
	then
		signal sqlstate '88888' set message_text = 'Invalid departure airport';
	end if;
	if new.destination_id not in (select airport_id
								  from airports)
	then
		signal sqlstate '88889' set message_text = 'Invalid destination airport';
	end if;
end;
//


create trigger Tri_airports_delete before delete on airports
for each row
begin
    delete from flights
    where departure_id = old.airport_id or destination_id = old.airport_id;
end;
//


create trigger Tri_tickets_delete before delete on tickets
for each row
begin
    update orders
    set status = 'Invalid'
    where orders.order_id = old.order_id;
    
    if old.class = '头等舱' then
        update flights
        set first_left = first_left + 1
        where old.flight_id = flights.flight_id and old.takeoff_time = flights.takeoff_time;    
    elseif old.class = '商务舱' then
        update flights
        set business_left = business_left + 1
        where old.flight_id = flights.flight_id and old.takeoff_time = flights.takeoff_time;
    elseif old.class = '经济舱' then
        update flights
        set economy_left = economy_left + 1
        where old.flight_id = flights.flight_id and old.takeoff_time = flights.takeoff_time;
    end if;
end;
//


create trigger Tri_tickets_insert before insert on tickets
for each row
begin
    if new.class = '头等舱' then
        update flights
        set first_left = first_left - 1
        where new.flight_id = flights.flight_id and new.takeoff_time = flights.takeoff_time;    
    elseif new.class = '商务舱' then
        update flights
        set business_left = business_left - 1
        where new.flight_id = flights.flight_id and new.takeoff_time = flights.takeoff_time;
    elseif new.class = '经济舱' then
        update flights
        set economy_left = economy_left - 1
        where new.flight_id = flights.flight_id and new.takeoff_time = flights.takeoff_time;
    end if;
end;
//


delimiter ;
