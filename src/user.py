from bottle import route,request 
from cassandra.cluster import Cluster
import uuid, collections, traceback, redis, thread, bcrypt, configparser, requests, sys, jsonpickle, random, os, zipfile, shutil, appcontext, permission 

config = configparser.ConfigParser()
config.read('config.ini')

def redis():
  return appcontext.redis()

def db():
  return appcontext.db()

def exists(username, password):
  usr = appcontext.db().execute('SELECT username, password, organization_uid from user_by_organization where username=%s', (username,))[0]
  match = usr.password == bcrypt.hashpw(password.encode('utf-8'), usr.password.encode('utf-8'))
  if match:
    return usr.organization_uid 
  return None

def create(organization_uid, username, password, firstName="", lastName=""):
  ins = "INSERT INTO user_by_organization (organization_uid, username, password) VALUES (%s,%s,%s);"
  db().execute(ins, (organization_uid, username, bcrypt.hashpw(password, bcrypt.gensalt())))
  ins = "INSERT INTO user (organization_uid, username) VALUES (%s,%s);"
  db().execute(ins, (organization_uid, username)) 
  permission.grant(username, 'USER:UPDATE:'+username)
  permission.grant(username, 'LOGIN')
  return ""

def update(organization_uid, username, password, firstName="", lastName=""):
  delete(organization_uid, username)
  create(organization_uid, username, password, firstName, lastName)
  return ""

def list(organization_uid):
  rows = appcontext.db().execute('SELECT username,organization_uid from user where organization_uid=%s', (organization_uid,))
  d = []
  for r in rows:
    d.insert(0,{'username':r.username,'organization_uid':str(r.organization_uid)})
  return d

def get(organization_uid, username):
  r = appcontext.db().execute('SELECT username,firstName,lastName,organization_uid from user where username=%s and organization_uid=%s', (username,organization_uid))
  d = {'username':r[0].username,'firstName':r[0].firstname,'lastName':r[0].lastname, 'organization_uid':r[0].organization_uid}
  return d

def delete(organization_uid, username):
  ins = "delete from user where username = %s and organization_uid=%s;"
  db().execute(ins, (username,organization_uid))
  ins = "delete from user_by_organization where organization_uid = %s and username = %s;" 
  db().execute(ins, (organization_uid,username)) 


