from ccmlib.cluster import Cluster


CLUSTER_PATH="."
cluster = Cluster(CLUSTER_PATH, 'functional-scenario', cassandra_version='2.2.1')

def cassandra(func):
  print("** STARTING **")
  cluster.populate(1).start()
  [node1] = cluster.nodelist()
  cluster.flush()
  try:
    func()
  except:
    print("failed to run functional test... ABORTING")
    cluster.remove()
    raise

  raw_input("Data Loaded Press enter to close...")
  cluster.remove()




