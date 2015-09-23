from bottle import route,request 
from cassandra.cluster import Cluster

import uuid, traceback, redis, thread, bcrypt, configparser, requests, sys, jsonpickle, random, os, zipfile, shutil 

config = configparser.ConfigParser()
config.read('config.ini')
rhost = config.get('redis','host')
rport = config.getint('redis','port')
rdb = config.getint('redis','db')
rdis = redis.StrictRedis(host=rhost, port=rport, db=rdb)
syskey = config.get('application','syskey')

keyspace = 'lms'
def session():
  return Cluster().connect(keyspace)

def callback(r, v):
    if r.query.get('callback') is not None:
        return '%s(%s)' % (r.query.get('callback'),v)
    else:
        return v

def from_json(arg):
  return jsonpickle.decode(arg)

def to_json(arg):
  return jsonpickle.encode(arg,unpicklable=False) 

@route('/version')
def sys_version():
  rdis.set('version','0.1.0')
  return callback(request,{'version':rdis.get('version')}) 

@route('/auth/status')
def auth_status():
  return callback(request,{'status':''})

@route('/auth/login', method='POST')
def auth_login():
  try:
    username = request.forms.get('username') 
    password = request.forms.get('password') 
    organization = uuid.UUID(request.forms.get('organization')) 

    if username is None or password is None:
      return callback(request,{'status':'INVALID'})

    usr = session().execute('SELECT username, password from user where username=%s and organization=%s', (username,organization))[0]
    match = usr.password == bcrypt.hashpw(password.encode('utf-8'), usr.password.encode('utf-8'))
    if match:
      key = "%s:%s" % (organization, uuid.uuid1())
      rdis.setex(key,2700,username)
      return callback(request,{'status':'SUCCESSFUL', 'session':key})
    return callback(request,{'status':'ERROR'})
  except Exception, e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return callback(request,{'status':'EXCEPTION', 'message':lines})

@route('/auth/logout')
def auth_login():
  return callback(request,{'status':'OK'})

@route('/sys')
def sys_hello():
  rows = session().execute('SELECT organization, username FROM user')
  d = [] 
  for r in rows:
    d.insert(0,{'organization':r.organization,'username':r.username})
  return to_json(d) 

