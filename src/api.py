from bottle import route,request 
from cassandra.cluster import Cluster

import configparser, thread, requests, sys, jsonpickle, random, os, zipfile, shutil 

config = configparser.ConfigParser()
config.read('config.ini')

cluster = Cluster()
session = cluster.connect('demo')

def from_json(arg):
  return jsonpickle.decode(arg)

def to_json(arg):
  return jsonpickle.encode(arg,unpicklable=False) 

@route('/sys')
def sys_hello():
  rows = session.execute('SELECT lastname, firstname, age FROM users')
  d = [] 
  for r in rows:
    d.insert(0,{'lastname':r.lastname,'firstname':r.firstname,'age':r.age})
  return to_json(d) 

