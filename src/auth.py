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


