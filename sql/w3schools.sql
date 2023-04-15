-- step 1 down
DROP TABLE IF EXISTS access_key CASCADE;

-- step 1 up
CREATE TABLE access_key(
    key_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- step 2 down
DROP TABLE IF EXISTS secured_resource CASCADE;

-- step 2 up
CREATE TABLE secured_resource(
    resource_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    is_open BOOL DEFAULT TRUE NOT NULL
);

-- step 3 down
DROP TABLE IF EXISTS security_group CASCADE;

-- step 3 up
CREATE TABLE security_group(
    group_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- step 4 down
DROP TABLE IF EXISTS group_key CASCADE;

-- step 4 up
CREATE TABLE group_key(
    group_id UUID REFERENCES security_group(group_id) ON DELETE CASCADE,
    key_id UUID REFERENCES access_key(key_id) ON DELETE CASCADE
);

-- step 5 down
DROP TABLE IF EXISTS group_resource CASCADE;

-- step 5 up
CREATE TABLE group_resource(
    group_id UUID REFERENCES security_group(group_id) ON DELETE CASCADE,
    resource_id UUID REFERENCES secured_resource(resource_id) ON DELETE CASCADE
);

-- step 6 down
DELETE FROM group_resource WHERE resource_id = (SELECT resource_id as r1 FROM secured_resource WHERE name = 'resource 1');
DELETE FROM group_key WHERE key_id = (SELECT key_id as k1 FROM access_key WHERE name = 'key 1');
DELETE FROM security_group WHERE name = 'group 1';
DELETE FROM secured_resource WHERE name = 'resource 1';
DELETE FROM access_key WHERE name = 'key 1';

-- step 6 up
INSERT INTO access_key(name) VALUES ('key 1');
INSERT INTO secured_resource(name) VALUES ('resource 1');
INSERT INTO security_group(name) VALUES ('group 1');
INSERT INTO group_key(group_id, key_id) SELECT group_id, key_id FROM security_group, access_key WHERE security_group.name = 'group 1' AND access_key.name = 'key 1';
INSERT INTO group_resource(group_id, resource_id) SELECT group_id, resource_id FROM security_group, secured_resource WHERE security_group.name = 'group 1' AND secured_resource.name = 'resource 1';
