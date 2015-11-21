from cassandra.cluster import Cluster
import random, os, uuid, jsonpickle

ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))

def to_json(arg):
  return jsonpickle.encode(arg,unpicklable=False) 

def test_insert():
  cluster = Cluster()
  session = cluster.connect()
  kscql = """
  CREATE KEYSPACE %s 
  WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
  """ % (ks)

  session.execute(kscql)

  session = cluster.connect(ks)
  organization_uid = str(uuid.uuid1())

  for name in os.listdir("cassandra"):
    if name.endswith(".cql"):
      with open("cassandra/" + name) as f:
        out = f.read()
        session.execute(out)

  insert = "insert into interaction (organization_uid, uid, url) values (%s, %s, %s)"
  session.execute(insert, (organization_uid, str(uuid.uuid1()), "http://google.com/?q=abc1"))
  session.execute(insert, (organization_uid, str(uuid.uuid1()), "http://google.com/?q=abc2"))
  session.execute(insert, (organization_uid, str(uuid.uuid1()), "http://google.com/?q=abc3"))

  rows = session.execute('SELECT organization_uid, uid, url FROM interaction')
  d = []
  for r in rows:
    d.insert(0,str(r.uid))

  insert = "insert into campaign (organization_uid, uid, type, interactions) values (%s,%s,%s,%s)"
  session.execute(insert, (organization_uid, str(uuid.uuid1()), 'type', set(d)))

  rows = session.execute('SELECT uid, type, interactions FROM campaign')
  d = []
  for r in rows:
    d.insert(0,{'id':r.uid,'type':r.type,'interactions':r.interactions})
    assert len(r.interactions) == 3
  print d 

