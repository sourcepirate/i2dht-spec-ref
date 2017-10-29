
import threading
from .bucket import KBuckets
from .node import Node, generate_id
from .server import DHTserver, Store, Ping, Pong, FindNode, FoundNode

class ThreadedServer(threading.Thread):

    def __init__(self, node, bucket):
        self.server = DHTserver(node, bucket, node.ip, node.port)
        super(ThreadedServer, self).__init__()

    def run(self):
        print("Starting the DHTServer .....")
        self.server.start()


def bootstrap(ip, port, bootstrap_node=[], find_node=None):
    mynodeid = generate_id()
    mynode = Node(mynodeid, ip, port)
    bucket = KBuckets(mynode)
    server = ThreadedServer(mynode, bucket)
    server.setDaemon(True)
    server.start()

    print(mynodeid)
    print(bootstrap_node)
    for node in bootstrap_node:
        print("Nodes are /../ ", node, mynode)
        action = Store(mynode, node, sender=mynode)
        action.execute(bucket)
        print("Done Node....")

    print("Proceeding to find node if any.....")

    if find_node:
        print("Trying to find node", find_node)
        action  = FindNode(int(find_node), sender=mynode)
        val = action.execute(bucket)
        print("Return", val)

    server.join()