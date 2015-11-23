from bottle import route,request 
from cassandra.cluster import Cluster
import uuid, collections, traceback, redis, thread, bcrypt, configparser, requests, sys, jsonpickle, random, os, zipfile, shutil, appcontext 

config = configparser.ConfigParser()
config.read('config.ini')

def redis():
  return appcontext.redis()

def db():
  return appcontext.db()

def exists(organization_uid, username, password):
  usr = appcontext.db().execute('SELECT username, password, organization_uid from user where username=%s', (username,))[0]
  match = usr.password == bcrypt.hashpw(password.encode('utf-8'), usr.password.encode('utf-8')) and usr.organization_uid == organization_uid
  return match

def create(organization_uid, username, password, firstName="", lastName=""):
  ins = "INSERT INTO user (organization_uid, username, password) VALUES (%s,%s,%s);"
  db().execute(ins, (organization_uid, username, bcrypt.hashpw(password, bcrypt.gensalt())))
  ins = "INSERT INTO user_by_organization (organization_uid, user_username) VALUES (%s,%s);"
  db().execute(ins, (organization_uid, username)) 
  return ""

def list(organization_uid):
  rows = appcontext.db().execute('SELECT user_username,organization_uid from user_by_organization where organization_uid=%s', (organization_uid,))
  d = []
  for r in rows:
    d.insert(0,{'username':r.user_username,'organization_uid':str(r.organization_uid)})
  return d

