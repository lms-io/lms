import random, os, uuid, bcrypt, sys, inspect, setup

from cassandra.cluster import Cluster
from webtest import TestApp


def test_insert():
  ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))
  session = setup.keyspace(ks)
  app = setup.app(ks) 
  organization_uid = uuid.uuid1()
  ins = "INSERT INTO user (organization_uid, username, password) VALUES (%s,%s,%s);"
  session.execute(ins, (organization_uid, 'joe', bcrypt.hashpw('bcrypt', bcrypt.gensalt())))
  session.execute(ins, (organization_uid, 'larry', bcrypt.hashpw('bcrypt', bcrypt.gensalt())))
  session.execute(ins, (organization_uid, 'moe', bcrypt.hashpw('bcrypt', bcrypt.gensalt())))
  rows = session.execute('SELECT username, password FROM user')
  d = [] 
  for r in rows:
    assert r.password == bcrypt.hashpw('bcrypt'.encode('utf-8'), r.password.encode('utf-8'))


def test_login():
  ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))
  session = setup.keyspace(ks)
  app = setup.app(ks) 
  organization_uid = uuid.uuid1()
  ins = "INSERT INTO user (organization_uid, username, password) VALUES (%s,%s,%s);"
  session.execute(ins, (organization_uid, 'joe', bcrypt.hashpw('password', bcrypt.gensalt())))
  res = app.get('/blah/auth/status') 
  print res.json.get('message')
  assert res.json.get('status') == 'ERROR'

  res = app.post('/auth/login', {'username':'joe','password':'wrongpass','organization_uid':organization_uid}) 
  print res.json.get('message')
  assert res.json.get('status') == 'ERROR'
  assert res.json.get('session') == None 

  res = app.post('/auth/login', {'username':'joe','password':'password','organization_uid':organization_uid}) 
  print res.json.get('message')
  assert res.json.get('status') == 'OK'
  key = res.json.get('session')
  assert key != None 

  res = app.get('/%s/auth/status' % (key,) ) 
  print res.json.get('message')
  assert res.json.get('status') == 'OK' 
  assert res.json.get('user') == 'joe' 

  res = app.get('/idontexist/auth/logout') 
  assert res.json.get('status') == 'ERROR' 

  res = app.get('/%s/auth/logout' % (key,) ) 
  print res.json.get('message')
  assert res.json.get('status') == 'OK' 

  res = app.get('/%s/auth/logout' % (key,) ) 
  assert res.json.get('status') == 'ERROR' 

  res = app.get('/%s/auth/status' % (key,) ) 
  assert res.json.get('status') == 'ERROR' 

def test_get_all_users():
  ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))
  session = setup.keyspace(ks)
  app = setup.app(ks) 
  organization_uid = uuid.uuid1()
  ins = "INSERT INTO user (organization_uid, username, password) VALUES (%s,%s,%s);"
  session.execute(ins, (organization_uid, 'joe', bcrypt.hashpw('password', bcrypt.gensalt())))

  res = app.post('/auth/login', {'username':'joe','password':'password','organization_uid':organization_uid}) 
  print res.json.get('message')
  assert res.json.get('status') == 'OK'
  key = res.json.get('session')
  assert key != None 

  res = app.get('/%s/users' % (key,) ) 
  print res.json.get('message')
  print res.json.get('res')
  assert res.json.get('status') == 'OK' 

