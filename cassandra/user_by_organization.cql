CREATE TABLE user_by_organization (
  organization_uid timeuuid primary key,
  user_username text,
  user_firstName text,
  user_lastName text
);
