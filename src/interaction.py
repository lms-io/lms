from bottle import route,request 
from cassandra.cluster import Cluster
import uuid, collections, traceback, redis, thread, bcrypt, configparser, requests, sys, jsonpickle, random, os, zipfile, shutil, appcontext, permission 

config = configparser.ConfigParser()
config.read('config.ini')

def redis():
  return appcontext.redis()

def db():
  return appcontext.db()

def create(organization_uid, name, url):
  interaction_uid = str(uuid.uuid1())
  ins = "INSERT INTO interaction (organization_uid,uid, name, url) VALUES (%s,%s,%s,%s);"
  db().execute(ins, (organization_uid, interaction_uid, name, url))

  return interaction_uid 

def update(organization_uid, interaction_uid, name, url):
  ins = "update interaction set name=%s, url=%s where uid=%s and organization_uid=%s;"
  db().execute(ins, (name, url, interaction_uid, organization_uid))

  return "" 

def list(organization_uid):
  rows = appcontext.db().execute('SELECT name,uid,organization_uid from interaction where organization_uid=%s', (organization_uid,))
  d = []
  for r in rows:
    d.insert(0,{'name':r.name,'uid':r.uid,'organization_uid':str(r.organization_uid)})
  return d

def get(organization_uid,uid):
  r = appcontext.db().execute('SELECT name, url, uid, organization_uid from interaction where uid=%s and organization_uid=%s', (uid,organization_uid))
  d = {'name':r[0].name,'url':r[0].url,'uid':r[0].uid, 'organization_uid':r[0].organization_uid}
  return d

def delete(organization_uid, interaction_uid):
  ins = "delete from interaction where uid = %s;"
  db().execute(ins, (interaction_uid,))

