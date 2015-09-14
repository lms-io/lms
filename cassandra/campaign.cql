CREATE TABLE campaign (
organization timeuuid,
id timeuuid,
type text,
interactions set<text>,
PRIMARY KEY (organization, id));


