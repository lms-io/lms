CREATE TABLE campaign (
organization_uid text primary key,
uid text,
type text,
interactions set<text>);


