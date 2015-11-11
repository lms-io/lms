from bottle import route,request 
from cassandra.cluster import Cluster
import uuid, collections, traceback, redis, thread, bcrypt, configparser, requests, sys, jsonpickle, random, os, zipfile, shutil, appcontext 

config = configparser.ConfigParser()
config.read('config.ini')

def redis():
  return appcontext.redis()

def db():
  return appcontext.db()


def create(name):
  organization_uid = uuid.uuid1()
  ins = "INSERT INTO organization (uid, name) VALUES (%s,%s);"
  db().execute(ins, (organization_uid, name)) 
  return organization_uid

def get(uid):
  org = db().execute('SELECT uid, name FROM organization where uid = %s',(uid,))[0]
  return {'uid':org.uid, 'name':org.name} 
