CREATE TABLE campaign (
  organization_uid text,
  uid text,
  name text,
  type text,
  interactions set<text>,
  PRIMARY KEY(organization_uid, uid)
);


