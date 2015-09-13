from cassandra.cluster import Cluster
import random, os

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

  for name in os.listdir("cassandra"):
    if name.endswith(".cql"):
      with open("cassandra/" + name) as f:
          out = f.read()
          session.execute(out)

  session.execute("""
  INSERT INTO user (username, password) VALUES ('joe', 'bcrypt');
          """)

  session.execute("""
  INSERT INTO user (username, password) VALUES ('frank', 'bcrypt');
          """)

  session.execute("""
  INSERT INTO user (username, password) VALUES ('larry', 'bcrypt');
          """)
  rows = session.execute('SELECT username, password FROM user')
  d = [] 
  for r in rows:
      d.insert(0,{'username':r.username,'password':r.password})
  print d


