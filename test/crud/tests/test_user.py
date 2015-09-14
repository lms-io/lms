from cassandra.cluster import Cluster
import random, os, bcrypt

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

  ins = "INSERT INTO user (username, password) VALUES ('%s', '%s');"
  session.execute(ins % ('joe', bcrypt.hashpw('bcrypt', bcrypt.gensalt())))
  session.execute(ins % ('larry', bcrypt.hashpw('bcrypt', bcrypt.gensalt())))
  session.execute(ins % ('moe', bcrypt.hashpw('bcrypt', bcrypt.gensalt())))

  rows = session.execute('SELECT username, password FROM user')
  d = [] 
  for r in rows:
    assert r.password == bcrypt.hashpw('bcrypt'.encode('utf-8'), r.password.encode('utf-8'))


