from cassandra.cluster import Cluster
import random

ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))

def test_insert():
  cluster = Cluster()
  session = cluster.connect()
  kscql = """
  CREATE KEYSPACE %s 
  WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
  """ % (ks)

  session.execute(kscql)

  session = cluster.connect(ks)
  session.execute("""
  CREATE TABLE users (
  firstname text,
  lastname text,
  age int,
  email text,
  city text,
  PRIMARY KEY (lastname));
  """)

  session.execute("""
  INSERT INTO users (firstname, lastname, age, email, city) VALUES ('John', 'Smith', 46, 'johnsmith@email.com', 'Sacramento');
          """)

  session.execute("""
  INSERT INTO users (firstname, lastname, age, email, city) VALUES ('Jane', 'Doe', 36, 'janedoe@email.com', 'Beverly Hills');
          """)

  session.execute("""
  INSERT INTO users (firstname, lastname, age, email, city) VALUES ('Rob', 'Byrne', 24, 'robbyrne@email.com', 'San Diego');
          """)

  rows = session.execute('SELECT lastname, firstname, age FROM users')
  d = [] 
  for r in rows:
      d.insert(0,{'lastname':r.lastname,'firstname':r.firstname,'age':r.age})
  print d


