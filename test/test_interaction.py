from cassandra.cluster import Cluster
import random, os, uuid

ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))

def test_insert():
  cluster = Cluster()
  session = cluster.connect()
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
  session.execute(insert, (organization, uuid.uuid1(), "http://google.com/?q=abc"))
  session.execute(insert, (organization, uuid.uuid1(), "http://google.com/?q=def"))
  session.execute(insert, (organization, uuid.uuid1(), "http://google.com/?q=ghi"))

  rows = session.execute('SELECT organization, id, url FROM interaction')
  d = [] 
  for r in rows:
    d.insert(0,{'id':r.id,'url':r.url})

  print d


