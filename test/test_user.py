import random, os, uuid, bcrypt, sys, inspect, setup

from cassandra.cluster import Cluster
from webtest import TestApp

ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))

def test_insert():
  session = setup.keyspace(ks)
  organization = uuid.uuid1()

  import main
  app = TestApp(main.init(ks))
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


