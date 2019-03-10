drop view if exists V_flight_info;
drop view if exists V_order_info;


create view V_flight_info(dept_city, dest_city, airline_name, flight_id, model_id, dept_airport, dept_datetime, dest_airport, dest_datetime, first_left, business_left, economy_left)
as
select DEP.city_name, DEST.city_name, airline_name, flight_id, model_id, DEP.airport_name, takeoff_time, DEST.airport_name, landing_time, first_left, business_left, economy_left
from flights F, airports DEP, airports DEST, airlines AL
where F.airline_id = AL.airline_id and F.departure_id = DEP.airport_id and F.destination_id = DEST.airport_id;


create view V_order_info(order_id,person_name, ticket_id, flight_id, flight_date, class, dept_airport, dest_airport)
as
select T.order_id, P.name, T.ticket_id, T.flight_id, F.takeoff_time, T.class, DEP.airport_name, DEST.airport_name
from flights F, tickets T, persons P, Orders O, airports DEP, airports DEST
where F.flight_id = T.flight_id and T.order_id = O.order_id and T.person_id = P.person_id and F.departure_id = DEP.airport_id and F.destination_id = DEST.airport_id and T.takeoff_time = F.takeoff_time;

