set search_path to s9999;

-- select count(*) from customers;
-- select * from customers;

select *
from customers
where city ilike '%or%'
  and coutry = 'USA'
order by city, postalcode;



select city, count(*) as customer_count
from customers
group by city;


-- select date('01-01-2024');
select extract(MONTH from date('2023-03-17'));
select extract(DAY from date('2023-03-17'));
select extract(DOW from date('2023-03-17'));


----------------

alter table orders
    add constraint fk_customerid
        FOREIGN KEY (customerid) REFERENCES customers (customerid)
            on delete cascade;

-- alter table shippers rename column "shipperID" to shipperid;
-- alter table shippers add primary key (shipperid);

alter table orders
    add constraint fk_shippers
        FOREIGN KEY (shipperid) REFERENCES shippers (shipperid)
            on delete cascade;


select *
from customers c,
     orders o
where c.customerid = o.customerid and
      c.coutry = 'USA' and extract(year from o.orderdate)=1996;


-- alter table employees rename column "employeeID" to employeeid;
alter table orderdetails rename column "productID" to productid;

-- alter table employees  add constraint pk_employee primary key (employeeid);
alter table orderdetails add constraint pk_orderdetails primary key (orderdetailid);
