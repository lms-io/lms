
import random, os, uuid, bcrypt, sys, inspect, setup, configparser

from cassandra.cluster import Cluster
from webtest import TestApp

config = configparser.ConfigParser()
config.read('config.ini')

syskey = config.get('application','syskey')

def test_insert():
  res = setup.app().post('/%s/organization' % (syskey,), {'name':'testcorp', 'admin_username':'course_test_insert', 'admin_password':'password'})
  organization_uid = str(res.json.get('uid'))

  res = setup.app().post('/auth/login', {'username':'course_test_insert','password':'password','organization_uid':organization_uid}) 
  key = res.json.get('session')

  res = setup.app().post('/%s/interaction' % (key,), {'name':'interaction1','url':'url','organization_uid':organization_uid}) 
  int1 = res.json.get('uid')

  res = setup.app().post('/%s/interaction' % (key,), {'name':'interaction2','url':'url','organization_uid':organization_uid}) 
  int2 = res.json.get('uid')

  res = setup.app().post('/%s/interaction' % (key,), {'name':'interaction3','url':'url','organization_uid':organization_uid}) 
  int3 = res.json.get('uid')

  res = setup.app().post('/%s/lesson' % (key,), {'name':'lesson1','url':'url','organization_uid':organization_uid, 'interactions':[int1]}) 
  less1 = res.json.get('uid')

  res = setup.app().post('/%s/lesson' % (key,), {'name':'lesson2','url':'url','organization_uid':organization_uid, 'interactions':[int2]}) 
  less2 = res.json.get('uid')

  res = setup.app().post('/%s/lesson' % (key,), {'name':'lesson3','url':'url','organization_uid':organization_uid, 'interactions':[int3]}) 
  less3 = res.json.get('uid')

  res = setup.app().post('/%s/course' % (key,), {'name':'mycourse','type':'type','organization_uid':organization_uid, 'lessons':[less1,less2,less3]}) 
  print res.json.get('message')
  print res.json.get('lessons')
  print res.json.get('status')

  course_uid = res.json.get('uid')
  print course_uid 

  res = setup.app().get('/%s/courses' % (key,) ) 
  print res.json.get('response')

  res = setup.app().get('/%s/course/%s' % (key,course_uid) ) 
  print res.json.get('message')
  print res.json.get('response')
  assert len(res.json.get('response').get('lessons')) == 3

  res = setup.app().post('/%s/course/%s' % (key,course_uid), {'name':'mycourse','type':'type','organization_uid':organization_uid, 'lessons':[less1,less2]}) 

  res = setup.app().get('/%s/course/%s' % (key,course_uid) ) 
  print res.json.get('message')
  print res.json.get('response')
  assert len(res.json.get('response').get('lessons')) == 2 

  res = setup.app().post('/%s/course/%s' % (key,course_uid), {'name':'mycourse','type':'type','organization_uid':organization_uid, 'lessons':[less1]}) 

  res = setup.app().get('/%s/course/%s' % (key,course_uid) ) 
  print res.json.get('message')
  print res.json.get('response')

  assert len(res.json.get('response').get('lessons')) == 1 
