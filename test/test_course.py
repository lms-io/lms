import random, os, uuid, bcrypt, sys, inspect, setup, configparser

from cassandra.cluster import Cluster
from webtest import TestApp

config = configparser.ConfigParser()
config.read('config.ini')

syskey = config.get('application','syskey')

def test_insert():
  res = setup.app().post('/%s/organization' % (syskey,), {'name':'testcorp', 'admin_username':'joe', 'admin_password':'password'})
  organization_uid = str(res.json.get('uid'))

  res = setup.app().post('/auth/login', {'username':'joe','password':'password','organization_uid':organization_uid}) 
  key = res.json.get('session')

  setup.app().post('/%s/course', {'name':'course1','type':'type','organization_uid':organization_uid}) 
  setup.app().post('/%s/course', {'name':'course2','type':'type','organization_uid':organization_uid}) 
  setup.app().post('/%s/course', {'name':'course3','type':'type','organization_uid':organization_uid}) 

  res = setup.app().get('/%s/courses' % (key,) ) 
  print res.json.get('message')
  assert res.json.get('status') == 'OK' 


def test_get_all_courses():
  res = setup.app().post('/%s/organization' % (syskey,), {'name':'testcorp', 'admin_username':'joe', 'admin_password':'password'})
  organization_uid = str(res.json.get('uid'))

  res = setup.app().post('/auth/login', {'username':'joe','password':'password','organization_uid':organization_uid}) 
  key = res.json.get('session')


  res = setup.app().get('/%s/courses' % (key,) ) 
  assert res.json.get('status') == 'OK' 

def test_update_course():
  res = setup.app().post('/%s/organization' % (syskey,), {'name':'testcorp', 'admin_username':'joe2', 'admin_password':'password'})
  organization_uid = str(res.json.get('uid'))

  res = setup.app().post('/auth/login', {'username':'joe2','password':'password'}) 
  key = res.json.get('session')

  res = setup.app().post('/%s/course' % (key,), {'name':'course14','type':'type2'}) 
  course_uid = str(res.json.get('uid'))
  res = setup.app().get('/%s/course/%s' % (key,course_uid) ) 
  print res.json
  print res.json.get('response')
  assert res.json.get('response').get('type') == 'type2'

  res = setup.app().post('/%s/course/%s' % (key,course_uid), {'name':'course14','type':'mynewtype'})
  print res.json.get('response')
  res = setup.app().get('/%s/course/%s' % (key,course_uid)) 
  print res.json.get('response')
  assert res.json.get('response').get('type') == 'mynewtype'
