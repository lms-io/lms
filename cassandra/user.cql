CREATE TABLE user (
  organization_uid timeuuid,
  username text primary key,
  firstName text,
  lastName text,
  password text
);
