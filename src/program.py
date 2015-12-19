from bottle import route,request 
from cassandra.cluster import Cluster
import uuid, collections, traceback, redis, thread, bcrypt, configparser, requests, sys, jsonpickle, random, os, zipfile, shutil, appcontext, permission 

config = configparser.ConfigParser()
config.read('config.ini')

def redis():
  return appcontext.redis()

def db():
  return appcontext.db()

def create(organization_uid, name):
  program_uid = str(uuid.uuid1())
  ins = "INSERT INTO program (organization_uid,uid, name) VALUES (%s,%s,%s);"
  db().execute(ins, (organization_uid, program_uid, name))

  return program_uid 

def update(organization_uid, program_uid, name):
  ins = "update program set name=%s where uid=%s and organization_uid=%s;"
  db().execute(ins, (name, program_uid, organization_uid))

  return "" 

def list(organization_uid):
  rows = appcontext.db().execute('SELECT name,uid,organization_uid from program where organization_uid=%s', (organization_uid,))
  d = []
  for r in rows:
    d.insert(0,{'name':r.name,'uid':r.uid,'organization_uid':str(r.organization_uid)})
  return d

def get(organization_uid,uid):
  r = appcontext.db().execute('SELECT name, uid, organization_uid from program where uid=%s and organization_uid=%s', (uid,organization_uid))
  d = {'name':r[0].name,'uid':r[0].uid, 'organization_uid':r[0].organization_uid}
  return d

def delete(organization_uid, program_uid):
  ins = "delete from program where uid = %s;"
  db().execute(ins, (program_uid,))

