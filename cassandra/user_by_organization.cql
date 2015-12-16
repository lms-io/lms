CREATE TABLE user_by_organization (
  organization_uid text,
  username text, 
  PRIMARY KEY(organization_uid, username)
);
