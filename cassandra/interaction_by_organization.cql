CREATE TABLE interaction_by_organization (
  organization_uid text,
  interaction_uid text,
  name text,
  PRIMARY KEY(organization_uid, interaction_uid)
);


