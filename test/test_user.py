import random, os, uuid, bcrypt, sys, inspect

from cassandra.cluster import Cluster
from webtest import TestApp

ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))
ks = 'lms'

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

  currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
  parentdir = os.path.dirname(currentdir)
  sys.path.insert(0,parentdir) 
  import main 
  app = TestApp(main.app)
  print app.get('/sys') 

  ins = "INSERT INTO user (organization, username, password) VALUES (%s,%s,%s);"
  session.execute(ins, (organization, 'joe', bcrypt.hashpw('bcrypt', bcrypt.gensalt())))
  session.execute(ins, (organization, 'larry', bcrypt.hashpw('bcrypt', bcrypt.gensalt())))
  session.execute(ins, (organization, 'moe', bcrypt.hashpw('bcrypt', bcrypt.gensalt())))

  print app.get('/sys') 
  assert False
  rows = session.execute('SELECT username, password FROM user')
  d = [] 
  for r in rows:
    assert r.password == bcrypt.hashpw('bcrypt'.encode('utf-8'), r.password.encode('utf-8'))

