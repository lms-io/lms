CREATE TABLE course (
  organization_uid text,
  uid text,
  name text,
  type text,
  lessons set<text>,
  PRIMARY KEY(organization_uid, uid)
);


