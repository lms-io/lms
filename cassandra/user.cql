CREATE TABLE user (
  organization_uid text,
  username text, 
  firstName text,
  lastName text,
  password text,
  PRIMARY KEY(username, organization_uid)
);

