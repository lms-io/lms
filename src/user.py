from bottle import route,request 
from cassandra.cluster import Cluster
import uuid, collections, traceback, redis, thread, bcrypt, configparser, requests, sys, jsonpickle, random, os, zipfile, shutil, appcontext 

config = configparser.ConfigParser()
config.read('config.ini')

def redis():
  return appcontext.redis()

def db():
  return appcontext.db()

def create(organization_uid, username, password):
  ins = "INSERT INTO user (organization_uid, username, password) VALUES (%s,%s,%s);"
  db().execute(ins, (organization_uid, username, bcrypt.hashpw(password, bcrypt.gensalt())))
  ins = "INSERT INTO user_by_organization (organization_uid, user_username) VALUES (%s,%s);"
  db().execute(ins, (organization_uid, username)) 
  return ""


