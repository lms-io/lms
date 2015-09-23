import random, os, uuid, bcrypt, sys, inspect, setup

from cassandra.cluster import Cluster
from webtest import TestApp


def test_insert():
  ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))
  session = setup.keyspace(ks)
  app = setup.app(ks) 
  organization = uuid.uuid1()
  ins = "INSERT INTO user (organization, username, password) VALUES (%s,%s,%s);"
  session.execute(ins, (organization, 'joe', bcrypt.hashpw('bcrypt', bcrypt.gensalt())))
  session.execute(ins, (organization, 'larry', bcrypt.hashpw('bcrypt', bcrypt.gensalt())))
  session.execute(ins, (organization, 'moe', bcrypt.hashpw('bcrypt', bcrypt.gensalt())))
  rows = session.execute('SELECT username, password FROM user')
  d = [] 
  for r in rows:
    assert r.password == bcrypt.hashpw('bcrypt'.encode('utf-8'), r.password.encode('utf-8'))


def test_login():
  ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))
  session = setup.keyspace(ks)
  app = setup.app(ks) 
  organization = uuid.uuid1()
  ins = "INSERT INTO user (organization, username, password) VALUES (%s,%s,%s);"
  session.execute(ins, (organization, 'joe', bcrypt.hashpw('password', bcrypt.gensalt())))
  res = app.get('/auth/status/blah') 
  assert res.json.get('status') == 'ERROR'

  res = app.post('/auth/login', {'username':'joe','password':'wrongpass','organization':organization}) 
  print res.json.get('message')
  assert res.json.get('status') == 'ERROR'
  assert res.json.get('session') == None 

  res = app.post('/auth/login', {'username':'joe','password':'password','organization':organization}) 
  print res.json.get('message')
  assert res.json.get('status') == 'SUCCESSFUL'
  key = res.json.get('session')
  assert key != None 

  res = app.get('/auth/status/%s' % (key,) ) 
  assert res.json.get('status') == 'OK' 
  assert res.json.get('user') == 'joe' 
