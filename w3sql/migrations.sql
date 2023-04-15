--v1.0
--upgrade
create table accesskey(
    keyid UUID DEFAULT gen_random_uuid() primary key,
    name text not null unique
);

--downgrade
drop table accesskey;

--v1.1
--upgrade
create table securedresources(
    resourceid UUID DEFAULT gen_random_uuid() primary key,
    name text not null unique,
    isopen bool default true not null
);

--downgrade
drop table securedresources;

--v1.2
--upgrade
create table securitygroup(
    groupid UUID DEFAULT gen_random_uuid() not null primary key,
    groupname text not null unique
);

--downgrade
drop table securitygroup;

--v1.3
--upgrade
create table group_key(
    groupid uuid references securitygroup(groupid) on delete cascade,
    keyid uuid references accesskey(keyid) on delete cascade
);
alter table group_key add constraint pk_group primary key (groupid, keyid);

--downgrade
alter table group_key drop constraint pk_group;
drop table group_key;

--v1.4
--upgrade
create table group_resource(
    groupid uuid unique references securitygroup(groupid) on delete cascade,
    resourceid uuid unique references securedresources(resourceid) on delete cascade
);
alter table group_resource add constraint pk_resourcegroup primary key (groupid, resourceid);

--downgrade
alter table group_resource drop constraint pk_resourcegroup;
drop table group_resource;

--v1.5
--upgrade
insert into accesskey(name) values ('test');
insert into accesskey(name) values ('test2');
insert into securedresources(name, isopen) values ('test1', true);
insert into securitygroup(groupname) values ('grupa1');

--downgrade
delete from securitygroup where securitygroup.groupname = 'grupa1';
delete from securedresources where securedresources.name = 'test1';
delete from accesskey where accesskey.name = 'test' or accesskey.name = 'test2';
