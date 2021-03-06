from ccmlib.cluster import Cluster
import pytest, os, inspect, sys, random

@pytest.fixture(scope="session", autouse=True)
def ccm_startup(request):

  ks = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))
  CLUSTER_PATH="."
  cluster = Cluster(CLUSTER_PATH, ks, cassandra_version='2.2.1')
  cluster.populate(1).start()
  [node1] = cluster.nodelist()

  # do some tests on the cluster/nodes. To connect to a node through thrift,
  # the host and port to a node is available through
  #   node.network_interfaces['thrift']

  cluster.flush()

  currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
  parentdir = os.path.dirname(currentdir)
  sys.path.insert(0,parentdir) 

  # do some other tests

  # after the test, you can leave the cluster running, you can stop all nodes
  # using cluster.stop() but keep the data around (in CLUSTER_PATH/test), or
  # you can remove everything with cluster.remove()
  def fin():
      cluster.remove()
  request.addfinalizer(fin)

