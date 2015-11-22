import random, os, uuid, bcrypt, sys, inspect, setup, configparser

from cassandra.cluster import Cluster
from webtest import TestApp

config = configparser.ConfigParser()
config.read('config.ini')

syskey = config.get('application','syskey')

def test_insert():
  ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))
  session = setup.keyspace(ks)
  app = setup.app(ks) 

  res = app.post('/%s/organization' % (syskey,), {'name':'testcorp', 'admin_username':'joe', 'admin_password':'password'})
  organization_uid = str(res.json.get('uid'))

  res = app.post('/auth/login', {'username':'joe','password':'password','organization_uid':organization_uid}) 
  key = res.json.get('session')

  app.post('/%s/user', {'username':'larry1','password':'password','organization_uid':organization_uid}) 
  app.post('/%s/user', {'username':'larry2','password':'password','organization_uid':organization_uid}) 
  app.post('/%s/user', {'username':'larry3','password':'password','organization_uid':organization_uid}) 

  res = app.get('/%s/users' % (key,) ) 
  print res.json.get('message')
  print res.json.get('res')
  assert res.json.get('status') == 'OK' 


def test_login():
  ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))
  session = setup.keyspace(ks)
  app = setup.app(ks) 
  res = app.post('/%s/organization' % (syskey,), {'name':'testcorp', 'admin_username':'joe', 'admin_password':'password'})
  organization_uid = str(res.json.get('uid'))

  print "organization : " + organization_uid
  res = app.get('/blah/auth/status') 
  print res.json.get('message')
  assert res.json.get('status') == 'EXCEPTION'

  res = app.post('/auth/login', {'username':'joe','password':'wrongpass','organization_uid':organization_uid}) 
  print res.json.get('message')
  assert res.json.get('status') == 'ERROR'
  assert res.json.get('session') == None 

  res = app.post('/auth/login', {'username':'joe','password':'password','organization_uid':organization_uid}) 
  key = res.json.get('session')
  assert res.json.get('status') == 'OK'
  assert key != None 

  res = app.get('/%s/auth/status' % (key,) ) 
  print res.json.get('message')
  assert res.json.get('status') == 'OK' 
  assert res.json.get('user') == 'joe' 

  res = app.get('/idontexist/auth/logout') 
  assert res.json.get('status') == 'EXCEPTION' 

  print key
  res = app.get('/%s/auth/logout' % (key,) ) 
  print res.json.get('message')
  assert res.json.get('status') == 'OK' 

  res = app.get('/%s/auth/logout' % (key,) ) 
  assert res.json.get('status') == 'EXCEPTION' 

  res = app.get('/%s/auth/status' % (key,) ) 
  assert res.json.get('status') == 'EXCEPTION' 

def test_get_all_users():
  ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))
  session = setup.keyspace(ks)
  app = setup.app(ks) 

  res = app.post('/%s/organization' % (syskey,), {'name':'testcorp', 'admin_username':'joe', 'admin_password':'password'})
  organization_uid = str(res.json.get('uid'))

  res = app.post('/auth/login', {'username':'joe','password':'password','organization_uid':organization_uid}) 
  print res.json.get('message')
  assert res.json.get('status') == 'OK'
  key = res.json.get('session')
  assert key != None 

  res = app.get('/%s/users' % (key,) ) 
  print res.json.get('message')
  print res.json.get('res')
  assert res.json.get('status') == 'OK' 

