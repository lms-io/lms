CREATE TABLE interaction (
  organization_uid text,
  uid text,
  name text,
  url text,
  PRIMARY KEY(uid, organization_uid)
);


