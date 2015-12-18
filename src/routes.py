from bottle import route,request 
from cassandra.cluster import Cluster

import uuid, collections, traceback, bcrypt, requests, sys, appcontext, auth, organization, user, interaction, permission 

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

# NON-SESSION 
@route('/version')
@err
def sys_version():
  appcontext.redis().set('version','0.1.0')
  return callback(request,{'version':appcontext.redis().get('version')}) 

# SUPER ADMIN
@route('/<key>/organization', method='POST')
@err
def admn_organization(key="" ): 
  if auth.is_sys(key) == False:
    return callback(res,{'status':'ERROR'})
  admin = request.forms.get('admin_username')
  adminpass = request.forms.get('admin_password')
  name = request.forms.get('name') 
  organization_uid = organization.create(name)
  user.create(organization_uid, admin, adminpass)
  permission.grant(admin, '*')
  return callback(request,{'uid':str(organization_uid)})

# AUTHORIZATION 
@route('/auth/login', method='POST')
@err
def auth_login():
  username = request.forms.get('username') 
  password = request.forms.get('password') 

  if username is None or password is None:
    return callback(request,{'status':'INVALID'})

  match = user.exists(username, password)

  if match:
    permission.has(username, ['LOGIN'])
    organization_uid = user.get(username).get('organization_uid')
    key = auth.createSession(organization_uid,username)
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
  auth.clearSession(key)
  return callback(request,{'status':'OK'})

# API 
@route('/<key>/users')
@err
def user_list(key=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['USER','USER:LIST'])

  organization_uid = s.get('organization_uid')
  res = user.list(organization_uid)   
  return callback(request,{'status':'OK', 'res':res})

@route('/<key>/user', method='POST')
@err
def user_add(key=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['USER','USER:CREATE'])

  username = request.forms.get('username') 
  password = request.forms.get('password') 
  firstName = request.forms.get('firstName') 
  lastName = request.forms.get('lastName') 
  organization_uid = s.get('organization_uid')
  user.create(organization_uid, username, password, firstName, lastName)
  return callback(request,{'status':'OK'})

@route('/<key>/user/<username>', method='GET')
@err
def user_view(key="", username=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['USER','USER:VIEW', 'USER:VIEW:'+username])

  ret = user.get(username)
  return callback(request,{'response':ret})

@route('/<key>/user/<username>', method='POST')
@err
def user_update(key="", username=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['USER','USER:UPDATE', 'USER:UPDATE:'+username])

  password = request.forms.get('password') 
  firstName = request.forms.get('firstName') 
  lastName = request.forms.get('lastName') 
  organization_uid = s.get('organization_uid')
  user.update(organization_uid, username, password, firstName, lastName)
  return callback(request,{'status':'OK'})

@route('/<key>/interactions')
@err
def interaction_list(key=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['INTERACTION','INTERACTION:LIST'])

  organization_uid = s.get('organization_uid')
  res = interaction.list(organization_uid)   
  return callback(request,{'status':'OK', 'res':res})

@route('/<key>/interaction/create', method='POST')
@err
def interaction_add(key=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['INTERACTION','INTERACTION:CREATE'])

  organization_uid = s.get('organization_uid')
  name = request.forms.get('name') 
  url = request.forms.get('url') 
  uid = interaction.create(organization_uid, name, url)
  return callback(request,{'uid':uid})

@route('/<key>/interaction/view/<uid>', method='GET')
@err
def interaction_view(key="", uid=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['INTERACTION','INTERACTION:VIEW', 'INTERACTION:VIEW:'+uid])

  ret = interaction.get(uid)
  return callback(request,{'response':ret})

@route('/<key>/interaction/update/<uid>', method='POST')
@err
def interaction_update(key="", uid=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['INTERACTION','INTERACTION:UPDATE', 'INTERACTION:UPDATE:'+uid])
  url = request.forms.get('url')
  name = request.forms.get('name')
  organization_uid = s.get('organization_uid')
  interaction.update(organization_uid, uid, name, url)
  ret = interaction.get(uid)
  return callback(request,{'status':'OK', 'response':ret})

