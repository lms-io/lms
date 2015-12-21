from bottle import route,request 
from cassandra.cluster import Cluster
import uuid, collections, traceback, redis, thread, bcrypt, configparser, requests, sys, jsonpickle, random, os, zipfile, shutil, appcontext, permission 

config = configparser.ConfigParser()
config.read('config.ini')

def redis():
  return appcontext.redis()

def db():
  return appcontext.db()

def create(organization_uid, name, type, lessons):
  course_uid = str(uuid.uuid1())
  ins = "INSERT INTO course (organization_uid,uid, name, type, lessons) VALUES (%s,%s,%s,%s,%s);"
  db().execute(ins, (organization_uid, course_uid, name, type, lessons))

  return course_uid 

def update(organization_uid, course_uid, name, type, lessons):
  ins = "update course set name=%s, type=%s, lessons=%s where uid=%s and organization_uid=%s;"
  db().execute(ins, (name, type, lessons, course_uid, organization_uid))

  return "" 

def list(organization_uid):
  rows = appcontext.db().execute('SELECT name,uid,organization_uid from course where organization_uid=%s', (organization_uid,))
  d = []
  for r in rows:
    d.insert(0,{'name':r.name,'uid':r.uid,'organization_uid':str(r.organization_uid)})
  return d

def get(organization_uid,uid):
  r = appcontext.db().execute('SELECT name, type, uid, lessons, organization_uid from course where uid=%s and organization_uid=%s', (uid,organization_uid))
  arr = []
  for o in r[0].lessons:
    arr.insert(0,o)


  d = {'name':r[0].name,'type':r[0].type,'uid':r[0].uid, 'organization_uid':r[0].organization_uid, 'lessons':arr}
  return d

def delete(organization_uid, course_uid):
  ins = "delete from course where uid = %s;"
  db().execute(ins, (course_uid,))

