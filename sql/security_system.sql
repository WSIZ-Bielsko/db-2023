set search_path to s9999;


create table accesskey(
    keyid serial primary key,
    name text not null unique
);

-- delete from accesskey where true;
insert into accesskey(name) values ('klucz2');

create table securedresource(
    resourceid serial primary key,
    name text not null unique,
    isopen bool default true not null
);


insert into securedresource(name) values ('sala 12');
insert into securedresource(name) values ('sala 05');


-- STEP 4

-- upgrade
create table securitygroup(
    groupid int not null,
    keyid int references accesskey(keyid),
    resourceid int references securedresource(resourceid)
);
alter table securitygroup add constraint pk_group primary key (keyid, resourceid);

-- downgrade
drop table securitygroup;




insert into securitygroup(groupid, keyid, resourceid) values (2, 5, 1);
