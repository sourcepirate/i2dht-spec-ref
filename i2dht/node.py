"""Node.py"""

import six
import struct
import random

def generate_id():
    return random.randint(0, 2**160 -1)


# class NodeID(object):

#     def __init__(self, _id):
#         self.id = _id

#     def __eq__(self, other):
#         return self.id == other.id

#     @classmethod
#     def generate(cls):
#         return cls(generate_id())

#     def __xor__(self, other):
#         distance = self.id ^ other.id
#         length = -1
#         while distance:
#             distance >>= 1
#             length += 1
#         return max(0, length)

#     def __str__(self):
#         return self.id


class Node(object):

    def __init__(self, _id, ip, port):
        self.ip = ip
        self.port = port
        self.id = _id

    def __eq__(self, other):
        return self.id == other._id

    def __xor__(self, other):
        distance = self.id ^ other.id
        length = -1
        while distance:
            distance >>= 1
            length += 1
        return max(0, length)
