import os, sys, inspect, fakeredis 
from cassandra.cluster import Cluster
from webtest import TestApp

def app(ks):
  from src import main
  r = fakeredis.FakeStrictRedis()
  app = TestApp(main.init(ks,r))
  return app

def keyspace(ks):
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

  return session 
