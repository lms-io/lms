from cassandra.cluster import Cluster
import redis

rdis = None 
def redis():
  return rdis 

keyspace = 'lms'
def db():
  return Cluster().connect(keyspace)


