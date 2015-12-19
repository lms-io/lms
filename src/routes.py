from bottle import route,request 
from cassandra.cluster import Cluster

import uuid, collections, traceback, bcrypt, requests, sys, appcontext, auth, organization, user, interaction, campaign, group, permission 

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

  organization_uid = user.exists(username, password)

  if organization_uid:
    permission.has(username, ['LOGIN'])
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

###############################################################################
# USER 
###############################################################################

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

  organization_uid = s.get('organization_uid')
  ret = user.get(organization_uid, username)
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

###############################################################################
# INTERACTION
###############################################################################

@route('/<key>/interactions')
@err
def interaction_list(key=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['INTERACTION','INTERACTION:LIST'])

  organization_uid = s.get('organization_uid')
  res = interaction.list(organization_uid)   
  return callback(request,{'status':'OK', 'res':res})

@route('/<key>/interaction', method='POST')
@err
def interaction_add(key=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['INTERACTION','INTERACTION:CREATE'])

  organization_uid = s.get('organization_uid')
  name = request.forms.get('name') 
  url = request.forms.get('url') 
  uid = interaction.create(organization_uid, name, url)
  return callback(request,{'uid':uid})

@route('/<key>/interaction/<uid>', method='GET')
@err
def interaction_view(key="", uid=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['INTERACTION','INTERACTION:VIEW', 'INTERACTION:VIEW:'+uid])

  organization_uid = s.get('organization_uid')
  ret = interaction.get(organization_uid,uid)
  return callback(request,{'response':ret})

@route('/<key>/interaction/<uid>', method='POST')
@err
def interaction_update(key="", uid=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['INTERACTION','INTERACTION:UPDATE', 'INTERACTION:UPDATE:'+uid])
  url = request.forms.get('url')
  name = request.forms.get('name')
  organization_uid = s.get('organization_uid')
  interaction.update(organization_uid, uid, name, url)
  ret = interaction.get(uid)
  return callback(request,{'status':'OK'})

###############################################################################
# CAMPAIGN
###############################################################################

@route('/<key>/campaigns')
@err
def campaign_list(key=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['CAMPAIGN','CAMPAIGN:LIST'])

  organization_uid = s.get('organization_uid')
  res = campaign.list(organization_uid)   
  return callback(request,{'status':'OK', 'res':res})

@route('/<key>/campaign', method='POST')
@err
def campaign_add(key=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['CAMPAIGN','CAMPAIGN:CREATE'])

  organization_uid = s.get('organization_uid')
  name = request.forms.get('name') 
  type = request.forms.get('type') 
  uid = campaign.create(organization_uid, name, type)
  return callback(request,{'uid':uid})

@route('/<key>/campaign/<uid>', method='GET')
@err
def campaign_view(key="", uid=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['CAMPAIGN','CAMPAIGN:VIEW', 'CAMPAIGN:VIEW:'+uid])

  organization_uid = s.get('organization_uid')
  ret = campaign.get(organization_uid,uid)
  return callback(request,{'response':ret})

@route('/<key>/campaign/<uid>', method='POST')
@err
def campaign_update(key="", uid=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['CAMPAIGN','CAMPAIGN:UPDATE', 'CAMPAIGN:UPDATE:'+uid])
  type = request.forms.get('type')
  name = request.forms.get('name')
  organization_uid = s.get('organization_uid')
  campaign.update(organization_uid, uid, name, type)
  ret = campaign.get(uid)
  return callback(request,{'status':'OK'})

###############################################################################
# GROUP
###############################################################################

@route('/<key>/groups')
@err
def group_list(key=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['GROUP','GROUP:LIST'])

  organization_uid = s.get('organization_uid')
  res = group.list(organization_uid)   
  return callback(request,{'status':'OK', 'res':res})

@route('/<key>/group', method='POST')
@err
def group_add(key=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['GROUP','GROUP:CREATE'])

  organization_uid = s.get('organization_uid')
  name = request.forms.get('name') 
  type = request.forms.get('type') 
  uid = group.create(organization_uid, name, type)
  return callback(request,{'uid':uid})

@route('/<key>/group/<uid>', method='GET')
@err
def group_view(key="", uid=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['GROUP','GROUP:VIEW', 'GROUP:VIEW:'+uid])

  organization_uid = s.get('organization_uid')
  ret = group.get(organization_uid,uid)
  return callback(request,{'response':ret})

@route('/<key>/group/<uid>', method='POST')
@err
def group_update(key="", uid=""):
  s = auth.session(key)
  permission.has(s.get('user'), ['GROUP','GROUP:UPDATE', 'GROUP:UPDATE:'+uid])
  type = request.forms.get('type')
  name = request.forms.get('name')
  organization_uid = s.get('organization_uid')
  group.update(organization_uid, uid, name, type)
  ret = group.get(uid)
  return callback(request,{'status':'OK'})

