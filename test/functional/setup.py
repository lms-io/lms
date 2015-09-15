from ccmlib.cluster import Cluster


CLUSTER_PATH="."
cluster = Cluster(CLUSTER_PATH, 'functional-scenario', cassandra_version='2.2.1')

def start():
  print("** STARTING **")
  cluster.populate(1).start()
  [node1] = cluster.nodelist()
  cluster.flush()



def stop():
  cluster.remove()


