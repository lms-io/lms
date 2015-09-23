import random, os, uuid, bcrypt, sys, inspect, setup

from cassandra.cluster import Cluster
from webtest import TestApp

ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))

def test_version():
  session = setup.keyspace(ks)
  app = setup.app(ks) 
  res = app.get('/version') 
  print res.json
  assert res.json.get('version') == "0.1.0"


