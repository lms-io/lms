import random, os, uuid, bcrypt, sys, inspect, setup, configparser

from cassandra.cluster import Cluster
from webtest import TestApp

config = configparser.ConfigParser()
config.read('config.ini')

syskey = config.get('application','syskey')

def test_insert():
  res = setup.app().post('/%s/organization' % (syskey,), {'name':'testcorp', 'admin_username':'lesson_test_insert', 'admin_password':'password'})
  organization_uid = str(res.json.get('uid'))

  res = setup.app().post('/auth/login', {'username':'lesson_test_insert','password':'password','organization_uid':organization_uid}) 
  key = res.json.get('session')

  res = setup.app().post('/%s/interaction' % (key,), {'name':'interaction1','url':'url','organization_uid':organization_uid}) 
  int1 = res.json.get('uid')

  res = setup.app().post('/%s/interaction' % (key,), {'name':'interaction2','url':'url','organization_uid':organization_uid}) 
  int2 = res.json.get('uid')

  res = setup.app().post('/%s/interaction' % (key,), {'name':'interaction3','url':'url','organization_uid':organization_uid}) 
  int3 = res.json.get('uid')

  res = setup.app().post('/%s/lesson' % (key,), {'name':'test_insert_lesson','type':'type','organization_uid':organization_uid, 'interactions':[int1,int2,int3]}) 
  print res.json.get('message')
  print res.json.get('interactions')
  print res.json.get('status')

  lesson_uid = res.json.get('uid')
  print lesson_uid 

  res = setup.app().get('/%s/lessons' % (key,) ) 
  print res.json.get('response')

  res = setup.app().get('/%s/lesson/%s' % (key,lesson_uid) ) 
  print res.json.get('message')
  print res.json.get('response')
  assert len(res.json.get('response').get('interactions')) == 3

  res = setup.app().post('/%s/lesson/%s' % (key,lesson_uid), {'name':'test_insert_lesson','type':'type','organization_uid':organization_uid, 'interactions':[int1,int2]}) 

  res = setup.app().get('/%s/lesson/%s' % (key,lesson_uid) ) 
  print res.json.get('message')
  print res.json.get('response')
  assert len(res.json.get('response').get('interactions')) == 2 

  res = setup.app().post('/%s/lesson/%s' % (key,lesson_uid), {'name':'test_insert_lesson','type':'type','organization_uid':organization_uid, 'interactions':[int1]}) 

  res = setup.app().get('/%s/lesson/%s' % (key,lesson_uid) ) 
  print res.json.get('message')
  print res.json.get('response')

  assert len(res.json.get('response').get('interactions')) == 1 
