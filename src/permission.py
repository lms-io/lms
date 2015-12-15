from bottle import route,request 
from cassandra.cluster import Cluster
import uuid, collections, traceback, redis, thread, bcrypt, configparser, requests, sys, jsonpickle, random, os, zipfile, shutil, appcontext 

config = configparser.ConfigParser()
config.read('config.ini')

def redis():
  return appcontext.redis()

def db():
  return appcontext.db()


def grant(user, permission):
  ins = "INSERT INTO user_permission (user, permission) VALUES (%s,%s);"
  db().execute(ins, (user, permission))
  return ""

def revoke(user, permission):
  ins = "delete from user_permission where user= %s and permission=%s;"
  db().execute(ins, (user, permission))
  return ""

def has(user, permissions):
  if _has(user, "*"):
    return True;
  for permission in set(permissions):
    if _has(user, permission):
      return True;
  raise ValueError('Permission Denied')

def _has(user, permission):
  ins = "select * from user_permission where user= %s and permission=%s;"
  rows = db().execute(ins, (user, permission))
  return len(rows) > 0 


