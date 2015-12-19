CREATE TABLE interaction_by_group (
  organization_uid text,
  uid text,
  name text,
  type text,
  interactions set<text>,
  PRIMARY KEY(organization_uid, uid)
);


