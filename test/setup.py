import random, os, sys, inspect, fakeredis 
from cassandra.cluster import Cluster
from webtest import TestApp

sys = {}
ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))

def app():
  if 'app' in sys.keys():
    return sys['app']

  from src import main
  r = fakeredis.FakeStrictRedis()
  cass = cassandra()
  app = TestApp(main.init(ks,r))
  sys['app'] = app
  return app

def cassandra():
  if 'session' in sys.keys():
    return sys['session']

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

  sys['session'] = session
  return session 
