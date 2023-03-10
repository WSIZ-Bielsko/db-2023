create table employees
(
    employee_id serial primary key,
    lastname    text not null,
    firstname   text not null,
    birthdate   date not null
);


insert into employees(employee_id, lastname, firstname, birthdate)
-- values (1,'Davolio','Nancy','1968-12-08');
-- values (2,'Fuller','Andrew','1952-02-19');
values (3,'Leverling','Janet','1963-08-30');
