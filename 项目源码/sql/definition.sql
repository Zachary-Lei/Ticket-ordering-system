/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2018/12/23 16:06:51                          */
/*==============================================================*/


drop table if exists admins;

drop table if exists tickets;

drop table if exists airports;

drop table if exists cities;

drop table if exists manages;

drop table if exists orders;

drop table if exists persons;

drop table if exists users;

drop table if exists flights;

drop table if exists airlines;

drop table if exists models;

/*==============================================================*/
/* Table: admins                                                */
/*==============================================================*/
create table admins
(
   admin_id             int not null,
   airline_id           char(2),
   admin_name           varchar(20),
   password             varchar(16),
   age                  int,
   gender               varchar(8),
   primary key (admin_id)
);

/*==============================================================*/
/* Table: airlines                                              */
/*==============================================================*/
create table airlines
(
   airline_id           char(2) not null,
   airline_name         varchar(50),
   primary key (airline_id)
);

/*==============================================================*/
/* Table: airports                                              */
/*==============================================================*/
create table airports
(
   airport_id           char(3) not null,
   city_name            varchar(20),
   airport_name         varchar(20),
   primary key (airport_id)
);

/*==============================================================*/
/* Table: cities                                                */
/*==============================================================*/
create table cities
(
   city_name            varchar(20) not null,
   city_eng             varchar(50),
   primary key (city_name)
);

/*==============================================================*/
/* Table: flights                                               */
/*==============================================================*/
create table flights
(
   flight_id            varchar(6) not null,
   model_id             varchar(10),
   airline_id           char(2),
   departure_id         char(3),
   destination_id       char(3),
   takeoff_time         datetime not null,
   landing_time         datetime,
   economy_price        int,
   business_price       int,
   first_price          int,
   economy_left         int,
   business_left        int,
   first_left           int,
   primary key (flight_id, takeoff_time)
);

/*==============================================================*/
/* Table: manages                                               */
/*==============================================================*/
create table manages
(
   person_id            varchar(20) not null,
   user_name            varchar(20) not null,
   primary key (person_id, user_name)
);

/*==============================================================*/
/* Table: models                                                */
/*==============================================================*/
create table models
(
   model_id             varchar(10) not null,
   first_total          int,
   business_total       int,
   economy_total        int,
   manufactor           varchar(20),
   primary key (model_id)
);

/*==============================================================*/
/* Table: orders                                                */
/*==============================================================*/
create table orders
(
   order_id             int not null,
   user_name            varchar(20),
   order_time           datetime default now(),
   status               varchar(10) default 'Processing',
   primary key (order_id)
);

/*==============================================================*/
/* Table: persons                                               */
/*==============================================================*/
create table persons
(
   person_id            varchar(20) not null,
   name                 varchar(20),
   age                  int,
   gender               varchar(8),
   primary key (person_id)
);

/*==============================================================*/
/* Table: tickets                                               */
/*==============================================================*/
create table tickets
(
   ticket_id            int not null auto_increment,
   person_id            varchar(20),
   order_id             int,
   flight_id            varchar(6),
   takeoff_time         datetime,
   class                varchar(8),
   primary key (ticket_id)
);

/*==============================================================*/
/* Table: users                                                 */
/*==============================================================*/
create table users
(
   user_name            varchar(20) not null,
   person_id            varchar(20),
   password             varchar(16),
   age                  int,
   gender               varchar(8),
   primary key (user_name)
);

alter table admins add constraint FK_Reference_10 foreign key (airline_id)
      references airlines (airline_id) on delete cascade on update cascade;

alter table airports add constraint FK_Reference_3 foreign key (city_name)
      references cities (city_name) on delete restrict on update restrict;

alter table flights add constraint FK_Reference_8 foreign key (model_id)
      references models (model_id) on delete restrict on update restrict;

alter table flights add constraint FK_Reference_9 foreign key (airline_id)
      references airlines (airline_id) on delete cascade on update cascade;

alter table manages add constraint FK_Reference_11 foreign key (user_name)
      references users (user_name) on delete cascade on update cascade;

alter table manages add constraint FK_Reference_2 foreign key (person_id)
      references persons (person_id) on delete cascade on update cascade;

alter table orders add constraint FK_Reference_12 foreign key (user_name)
      references users (user_name) on delete cascade on update cascade;

alter table tickets add constraint FK_Reference_13 foreign key (flight_id, takeoff_time)
      references flights (flight_id, takeoff_time) on delete cascade on update cascade;

alter table tickets add constraint FK_Reference_4 foreign key (person_id)
      references persons (person_id) on delete restrict on update restrict;

alter table tickets add constraint FK_Reference_6 foreign key (order_id)
      references orders (order_id) on delete restrict on update restrict;

alter table users add constraint FK_Reference_14 foreign key (person_id)
      references persons (person_id) on delete restrict on update restrict;
      
/*Foreign key index*/
create index Idx_airports_city_name on airports(city_name ASC);
create index Idx_orders_user_name on orders(user_name ASC);
create index Idx_admins_airline_id on admins(airline_id ASC);
create index Idx_flights_airline_id on flights(airline_id ASC);
create index Idx_flights_model_id on flights(model_id ASC);
create index Idx_tickets_person_id on tickets(person_id ASC);
create index Idx_tickets_order_id on tickets(order_id ASC);
create index Idx_tickets_flights on tickets(flight_id, takeoff_time);
create index Idx_users_person_id on users(person_id ASC);
