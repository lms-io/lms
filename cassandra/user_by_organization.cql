CREATE TABLE user_by_organization (
  organization_uid text,
  username text, 
  password text,
  PRIMARY KEY(username, organization_uid)
);
