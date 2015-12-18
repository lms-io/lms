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

  setup.app().post('/%s/interaction/create', {'name':'interaction1','url':'url','organization_uid':organization_uid}) 
  setup.app().post('/%s/interaction/create', {'name':'interaction2','url':'url','organization_uid':organization_uid}) 
  setup.app().post('/%s/interaction/create', {'name':'interaction3','url':'url','organization_uid':organization_uid}) 

  res = setup.app().get('/%s/interactions' % (key,) ) 
  print res.json.get('message')
  assert res.json.get('status') == 'OK' 


def test_get_all_interactions():
  res = setup.app().post('/%s/organization' % (syskey,), {'name':'testcorp', 'admin_username':'joe', 'admin_password':'password'})
  organization_uid = str(res.json.get('uid'))

  res = setup.app().post('/auth/login', {'username':'joe','password':'password','organization_uid':organization_uid}) 
  key = res.json.get('session')


  res = setup.app().get('/%s/interactions' % (key,) ) 
  assert res.json.get('status') == 'OK' 

def test_update_interaction():
  res = setup.app().post('/%s/organization' % (syskey,), {'name':'testcorp', 'admin_username':'joe2', 'admin_password':'password'})
  organization_uid = str(res.json.get('uid'))

  res = setup.app().post('/auth/login', {'username':'joe2','password':'password'}) 
  key = res.json.get('session')

  res = setup.app().post('/%s/interaction/create' % (key,), {'name':'interaction14','url':'url2'}) 
  interaction_uid = str(res.json.get('uid'))
  res = setup.app().get('/%s/interaction/view/%s' % (key,interaction_uid) ) 
  print res.json.get('response')
  assert res.json.get('response').get('url') == 'url2'

  res = setup.app().post('/%s/interaction/update/%s' % (key,interaction_uid), {'name':'interaction14','url':'mynewurl'})
  print res.json.get('response')
  res = setup.app().get('/%s/interaction/view/%s' % (key,interaction_uid)) 
  print res.json.get('response')
  assert res.json.get('response').get('url') == 'mynewurl'
