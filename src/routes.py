from bottle import route,request 
from cassandra.cluster import Cluster

import uuid, collections, traceback, thread, bcrypt, configparser, requests, sys, jsonpickle, random, os, zipfile, shutil, appcontext, auth, organizationdao 

config = configparser.ConfigParser()
config.read('config.ini')

def callback(r, v):
    if r.query.get('callback') is not None:
        return '%s(%s)' % (r.query.get('callback'),v)
    else:
        return v

@route('/<key>/organization', method='POST')
def admn_organization(key=""): 
  try:
    if auth.is_sys(key) == False:
      return callback(res,{'status':'ERROR'})

    name = request.forms.get('name') 
    res = organizationdao.create(name)
    return callback(request,{'uid':str(res)})
  except Exception, e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return callback(request,{'status':'EXCEPTION', 'message':lines})

@route('/version')
def sys_version():
  try:
    appcontext.redis().set('version','0.1.0')
    return callback(request,{'version':appcontext.redis().get('version')}) 
  except Exception, e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return callback(request,{'status':'EXCEPTION', 'message':lines})

@route('/auth/login', method='POST')
def auth_login():
  try:
    username = request.forms.get('username') 
    password = request.forms.get('password') 
    organization_uid = uuid.UUID(request.forms.get('organization_uid')) 

    if username is None or password is None:
      return callback(request,{'status':'INVALID'})

    usr = appcontext.db().execute('SELECT username, password, organization_uid from user where username=%s', (username,))[0]
    match = usr.password == bcrypt.hashpw(password.encode('utf-8'), usr.password.encode('utf-8')) and usr.organization_uid == organization_uid
    if match:
      key = "%s:%s" % (organization_uid, uuid.uuid1())
      appcontext.redis().setex(key,2700,username)
      return callback(request,{'status':'OK', 'session':key})
    return callback(request,{'status':'ERROR'})
  except Exception, e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return callback(request,{'status':'EXCEPTION', 'message':lines})

@route('/<key>/auth/status')
def auth_status(key=""):
  try:
    s = auth.session(key) 
    if s == None:
      return callback(request,{'status':'ERROR'})

    return callback(request,{'status':'OK','user': s.get('user')})
  except Exception, e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return callback(request,{'status':'EXCEPTION', 'message':lines})

@route('/<key>/auth/logout')
def auth_logout(key=""):
  try:
    session = appcontext.redis().get(key)
    if session == None:
      return callback(request,{'status':'ERROR'})

    session = appcontext.redis().delete(key)
    return callback(request,{'status':'OK'})
  except Exception, e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return callback(request,{'status':'EXCEPTION', 'message':lines})

@route('/<key>/users')
def auth_status(key=""):
  try:
    s = auth.session(key) 
    if s == None:
      return callback(request,{'status':'ERROR'})

    user = s.get('user')
    organization_uid = s.get('organization_uid')

    rows = appcontext.db().execute('SELECT user_username,organization_uid from user_by_organization where organization_uid=%s', (organization_uid,))
    d = []
    for r in rows:
      d.insert(0,{'username':r.user_username,'organization_uid':str(r.organization_uid)})
      
    return callback(request,{'status':'OK', 'res':d})
  except Exception, e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return callback(request,{'status':'EXCEPTION', 'message':lines})



