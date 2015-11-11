from bottle import route,request 
from cassandra.cluster import Cluster

import uuid, collections, traceback, bcrypt, requests, sys, appcontext, auth, organizationdao 

def callback(r, v):
  if r.query.get('callback') is not None:
    return '%s(%s)' % (r.query.get('callback'),v)
  else:
    return v

def err(func):
  def wrapper(*args, **kwargs):
    try:
      result = func(*args, **kwargs)
      return result 
    except Exception, e:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      return {'status':'EXCEPTION', 'message':lines}
  return wrapper

@route('/version')
@err
def sys_version():
  appcontext.redis().set('version','0.1.0')
  return callback(request,{'version':appcontext.redis().get('version')}) 

@route('/auth/login', method='POST')
@err
def auth_login():
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
  
@route('/<key>/auth/status')
@err
def auth_status(key=""):
  s = auth.session(key) 
  return callback(request,{'status':'OK','user': s.get('user')})

@route('/<key>/auth/logout')
@err
def auth_logout(key=""):
  appcontext.redis().delete(key)
  return callback(request,{'status':'OK'})

@route('/<key>/organization', method='POST')
@err
def admn_organization(key=""): 
  if auth.is_sys(key) == False:
    return callback(res,{'status':'ERROR'})
  name = request.forms.get('name') 
  res = organizationdao.create(name)
  return callback(request,{'uid':str(res)})

@route('/<key>/users')
@err
def auth_status(key=""):
  s = auth.session(key) 
  user = s.get('user')
  organization_uid = s.get('organization_uid')
  rows = appcontext.db().execute('SELECT user_username,organization_uid from user_by_organization where organization_uid=%s', (organization_uid,))
  d = []
  for r in rows:
    d.insert(0,{'username':r.user_username,'organization_uid':str(r.organization_uid)})
    
  return callback(request,{'status':'OK', 'res':d})


