from ccmlib.cluster import Cluster
import pytest

@pytest.fixture(scope="session", autouse=True)
def ccm_startup(request):
    CLUSTER_PATH="."
    cluster = Cluster(CLUSTER_PATH, 'hello-world-test', cassandra_version='2.2.1')
    cluster.populate(1).start()
    [node1] = cluster.nodelist()

    # do some tests on the cluster/nodes. To connect to a node through thrift,
    # the host and port to a node is available through
    #   node.network_interfaces['thrift']

    cluster.flush()

    # do some other tests

    # after the test, you can leave the cluster running, you can stop all nodes
    # using cluster.stop() but keep the data around (in CLUSTER_PATH/test), or
    # you can remove everything with cluster.remove()
    def fin():
        cluster.remove()
    request.addfinalizer(fin)

