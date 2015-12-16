CREATE TABLE interaction_by_user (
  organization_uid text,
  interaction_uid text,
  username text,
  uid text,
  name text,
  status text,
  url text,
  PRIMARY KEY(username, uid)
);

