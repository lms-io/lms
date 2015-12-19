from bottle import route,request 
from cassandra.cluster import Cluster
import uuid, collections, traceback, redis, thread, bcrypt, configparser, requests, sys, jsonpickle, random, os, zipfile, shutil, appcontext, permission 

config = configparser.ConfigParser()
config.read('config.ini')

def redis():
  return appcontext.redis()

def db():
  return appcontext.db()

def create(organization_uid, name, type):
  group_uid = str(uuid.uuid1())
  ins = "INSERT INTO interaction_by_group (organization_uid,uid, name, type) VALUES (%s,%s,%s,%s);"
  db().execute(ins, (organization_uid, group_uid, name, type))

  return group_uid 

def update(organization_uid, group_uid, name, type):
  ins = "update interaction_by_group set name=%s, type=%s where uid=%s and organization_uid=%s;"
  db().execute(ins, (name, type, group_uid, organization_uid))

  return "" 

def list(organization_uid):
  rows = appcontext.db().execute('SELECT name,uid,organization_uid from interaction_by_group where organization_uid=%s', (organization_uid,))
  d = []
  for r in rows:
    d.insert(0,{'name':r.name,'uid':r.uid,'organization_uid':str(r.organization_uid)})
  return d

def get(organization_uid,uid):
  r = appcontext.db().execute('SELECT name, type, uid, organization_uid from interaction_by_group where uid=%s and organization_uid=%s', (uid,organization_uid))
  d = {'name':r[0].name,'type':r[0].type,'uid':r[0].uid, 'organization_uid':r[0].organization_uid}
  return d

def delete(organization_uid, group_uid):
  ins = "delete from interaction_by_group where uid = %s;"
  db().execute(ins, (group_uid,))

