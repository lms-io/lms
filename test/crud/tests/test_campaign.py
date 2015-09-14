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

  for name in os.listdir("cassandra"):
    if name.endswith(".cql"):
      with open("cassandra/" + name) as f:
          out = f.read()
          session.execute(out)

  insert = "insert into interaction (id, url) values (%s, '%s')"
  session.execute(insert % (str(uuid.uuid1()), "http://google.com/?q=abc"))
  session.execute(insert % (str(uuid.uuid1()), "http://google.com/?q=def"))
  session.execute(insert % (str(uuid.uuid1()), "http://google.com/?q=ghi"))

  rows = session.execute('SELECT id, url FROM interaction')
  d = []
  for r in rows:
      d.insert(0,str(r.id))

  insert = "insert into campaign (id, type, interactions) values (%s,'blah',%s)"
  # need to make this work in a way that isn't ridiculous
  lst = to_json(d).replace('[','{').replace(']','}').replace('"', "'")
  qry = insert % (str(uuid.uuid1()), lst) 
  print qry 
  session.execute(qry)

  rows = session.execute('SELECT id, type, interactions FROM campaign')
  d = []
  for r in rows:
    d.insert(0,{'id':r.id,'type':r.type,'interactions':r.interactions})
    assert len(r.interactions) == 3
  print d 

