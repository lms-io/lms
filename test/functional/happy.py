from cassandra.cluster import Cluster
import random, os, uuid, bcrypt, setup 

setup.start()

cluster = Cluster()
session = cluster.connect()
ks = "functionaltest"
kscql = """
CREATE KEYSPACE %s 
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
""" % (ks)
session.execute(kscql)

session = cluster.connect(ks)
organization = uuid.uuid1()

for name in os.listdir("cassandra"):
  if name.endswith(".cql"):
    with open("cassandra/" + name) as f:
      out = f.read()
      session.execute(out)

insert = "insert into interaction (organization, id, url) values (%s, %s, %s)"
session.execute(insert, (organization, uuid.uuid1(), "http://google.com/?q=abc1"))
session.execute(insert, (organization, uuid.uuid1(), "http://google.com/?q=abc2"))
session.execute(insert, (organization, uuid.uuid1(), "http://google.com/?q=abc3"))

rows = session.execute('SELECT organization, id, url FROM interaction')
d = []
for r in rows:
  d.insert(0,str(r.id))

insert = "insert into campaign (organization, id, type, interactions) values (%s,%s,%s,%s)"
session.execute(insert, (organization, uuid.uuid1(), 'type', set(d)))


raw_input("Data Loaded Press enter to close...")
setup.stop()
