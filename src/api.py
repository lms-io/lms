from bottle import route,request 
from cassandra.cluster import Cluster

import thread, requests, sys, jsonpickle, random, os, zipfile, shutil 

keyspace = 'lms'

def session():
  return Cluster().connect(keyspace)

def from_json(arg):
  return jsonpickle.decode(arg)

def to_json(arg):
  return jsonpickle.encode(arg,unpicklable=False) 

@route('/sys')
def sys_hello():
  rows = session().execute('SELECT organization, username FROM user')
  d = [] 
  for r in rows:
    d.insert(0,{'organization':r.organization,'username':r.username})
  return to_json(d) 

