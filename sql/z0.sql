-- tworzenie tabel
create table t1
(
    id     serial primary key,
    name   text not null,
    active boolean default True
);


-- do id można wykorzystać `id UUID DEFAULT gen_random_uuid() PRIMARY KEY`

-- dodawanie rekordów
insert into t1(name, active)
values ('kadabra', FALSE);


-- wyszukiwanie w tabeli
select * from t1 where active = True;
