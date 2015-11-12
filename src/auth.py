import configparser, appcontext, uuid 

config = configparser.ConfigParser()
config.read('config.ini')

syskey = config.get('application','syskey')
def is_sys(key):
  return key == syskey

def session(key):
  rdis = appcontext.redis()
  user = rdis.get(key)
  if user == None:
    raise ValueError('User not found')

  rdis.setex(key,2700,user)
  organization_uid = uuid.UUID(key.split(":")[0])
  return {'key':key,'user':user,'organization_uid':organization_uid}

def clearSession(key):
  rdis = appcontext.redis()
  #checks to see if it matches the syntax of a valid session
  #otherwise users could simply delete all keys in redis :(
  user = rdis.get(key)
  if user == None:
    raise ValueError('User not found')
  organization_uid = uuid.UUID(key.split(":")[0])
  uid = uuid.UUID(key.split(":")[1])
  #create the session key the same way it is done via create sesion
  key = "%s:%s" % (organization_uid, uid)
  appcontext.redis().delete(key)

def createSession(organization_uid,username):
  rdis = appcontext.redis()
  key = "%s:%s" % (organization_uid, uuid.uuid1())
  rdis.setex(key,2700,username)
  return key
