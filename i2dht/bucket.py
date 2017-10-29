
import threading
import heapq
from .node import Node

MAX_BUCKETS = 20
ID_LENGTH = 160
DEFAULF_LIMIT = 10


class KBuckets(object):

    def __init__(self, mynode, k_size=MAX_BUCKETS,  id_length=ID_LENGTH):
        """Implementing in kbuckets"""
        self.id = mynode
        self.ksize = k_size
        self._buckets = [list() for i in range(id_length)]
        self.lock = threading.Lock()

    def insert(self, peer):
        
        bucket_index = self.id ^ peer
        index_triple = (peer.id, peer.ip, peer.port)
        with self.lock:
            bucket = self._buckets[bucket_index]
            if index_triple in bucket:
                bucket.pop(index_triple)
            elif len(bucket) >= self.ksize:
                bucket.pop(0) # Should apply peer retension policy. Can be ignored for now since this is a reference implementation
            bucket.append(index_triple)
            print("New peer in ::", bucket_index)
    
    def __getitem__(self, p):
        with self.lock:
            peers = (peer for bucket in self._buckets for peer in bucket)
            best_peers = heapq.nsmallest(DEFAULF_LIMIT, peers, lambda x: p ^ x[0])
            return [Node(*_peer) for _peer in best_peers]