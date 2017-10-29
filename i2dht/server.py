
import socket
import json
from .node import Node
from .bucket import KBuckets
from threading import Lock


class SocketMixin(object):

    def send_data(self, _connect_pair, dict_data):
        print("Trying to send data......")
        try:
            _socket = socket.socket(socket.AF_INET)
            print("Connecting ..... ", _connect_pair)
            _socket.connect(_connect_pair)
            _socket.settimeout(5.0)
            _json_string = json.dumps(dict_data)
            print("Data Sending....", _json_string)
            _socket.sendall(_json_string.encode('utf-8'))
            data = _socket.recv(4096)
            if not data:
                return None
            print("Data recived.... ", data)
            return json.loads(data.decode('utf-8'))
        except socket.timeout:
            print("Timeout for response")
            return None
        except socket.error as e:
            raise Exception(str(e))


class Command(dict, SocketMixin):

    def __init__(self, command_name, sender=None, payload={}, **kwargs):
        self.cmd = command_name
        self.sender = sender
        print("Sender is ...{}".format(self.sender))
        self.payload = payload,
        self.kwargs = kwargs
        super(Command, self).__init__({
            "cmd": self.cmd,
            "rpc_id": self.sender.id,
            "rpc_ip": self.sender.ip,
            "rpc_port": self.sender.port,
            "payload": self.payload
        })

    def do(self):
        pass

    def handle(self, bucket):
        pass

    def execute(self, bucket):
        print(self)
        self.handle(bucket)
        return self.do()


class Ping(Command):

    def __init__(self, node, sender=None):
        self.node = node
        super(Ping, self).__init__("ping", payload={
            "node_id": node.id,
        }, sender=sender)

    def do(self):
        return self.send_data((self.node.ip, self.node.port), self)


class FindNode(Command):

    def __init__(self, node, sender=None):
        self.node = node
        super(FindNode, self).__init__("findnode", payload={
            "node_id": node
        }, sender=sender)

    def handle(self, bucket):
        print(bucket._buckets)
        nearest_nodes = bucket[self.node]
        print(nearest_nodes)
        lock = Lock()
        for near in nearest_nodes:
            print("nearest_nodes", near)
            if near.id == self.node:
                return {"payload": {"found": True, "data": {"id": near.id, "ip": near.ip, "port": near.port}}}
            found = self.find_node(near, lock=lock)
            return found
        return None

    def find_node(self, node, lock=None):
        with lock:
            data = self.send_data((node.ip, node.port), self)
            return data

    def execute(self, bucket):
        print(self)
        return self.handle(bucket)

    @classmethod
    def from_payload_dict(cls, sender, payload):
        print(payload)
        return cls(payload[0]["node_id"], sender=sender)


class Store(Command):

    def __init__(self, _from, _to, sender=None):
        self._from = _from
        self._to = _to
        super(Store, self).__init__("store", payload=dict(
            id=self._from.id,
            ip=self._from.ip,
            port=self._from.port
        ), sender=sender)

    def do(self):
        print("Self is: ",self)
        rpc = self.send_data((self._to[1], self._to[2]), self)
        if rpc:
            return rpc
        return None

    def handle(self, bucket):
        stored_node = Node(self._to[0], self._to[1], self._to[2])
        bucket.insert(stored_node)


class Pong(Command):

    def __init__(self, sender=None):
        super(Pong, self).__init__("pong", payload={
            "success": True
        }, sender=sender)

    def do(self):
        return self.send_data((self.sender.ip, self.sender.port), self)


class FoundNode(Command):

    def __init__(self, node, sender=None):
        self.found = node
        super(FoundNode, self).__init__("foundnode", payload={
            "found": True,
            "data": {
                "id": self.found.id,
                "ip": self.found.ip,
                "port": self.found.port
            }
        }, sender=sender)

    def do(self):
        return self.send_data((self.sender.ip, self.sender.port), self)

    @classmethod
    def from_payload_dict(cls, sender, payload):
        return cls(Node(payload["data"]["id"], payload["data"]["ip"], payload["data"]["port"]), sender=sender)


class DoneStoring(Command):

    def __init__(self, stored, sender=None):
        self.stored = stored
        super(DoneStoring, self).__init__("donestoring", payload={
            "id": self.stored.id,
            "ip": self.stored.ip,
            "port": self.stored.port
        }, sender=sender)

    def do(self):
        return self.send_data((self.sender.ip, self.sender.port), self)

    def handle(self, bucket):
        bucket.insert(self.stored)

    @classmethod
    def from_payload_dict(cls, sender, payload):
        print(type(payload))
        return cls(Node(payload["id"], payload["ip"], payload["port"]), sender=sender)


class SocketServer(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):

        _socket = socket.socket(socket.AF_INET)
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _socket.bind((self.host, self.port))
        _socket.listen(10)

        while True:
            connection, address = _socket.accept()
            _request = {"sender": {"ip": address[0], "port": address[1]}}
            print(address)
            value = connection.recv(4096)
            value = value.decode('utf-8')
            print("Value is ", value)
            _data = json.loads(value)
            _request["sender"]["id"] = _data["rpc_id"]
            _request.update({
                "sender": Node(_data["rpc_id"], _data["rpc_ip"], _data["rpc_port"]),
                "cmd": _data["cmd"],
                "payload": _data["payload"]
            })
            self.handle(_request)

    def handle(self, data):
        pass


class DHTserver(SocketServer):

    def __init__(self, node, bucket, host, port):
        self.node = node
        self.kbucket = bucket
        super(DHTserver, self).__init__(host, port)

    def handle(self, data):

        cmd = data["cmd"]
        sender = data["sender"]
        payload = data["payload"]

        print("Got New Request:")
        print(cmd, sender, payload)

        if cmd == "ping":
            action = Pong(sender=sender)
            action.execute(self.kbucket)
        elif cmd == "findnode":
            print("Got New command")
            action = FindNode.from_payload_dict(sender, payload)
            print("Trying to find node....{}".format(payload[0]["node_id"]))
            new_payload = action.execute(self.kbucket)
            print(new_payload)
            new_action = FoundNode.from_payload_dict(sender,new_payload["payload"])
            data = new_action.execute(self.kbucket)
        elif cmd == "foundnode":
            print("Payload:", payload)
            print("Found node....{}".format(payload[0]["data"]["id"]))
            # new_action = FoundNode.from_payload_dict(sender, payload[0]["data"])
            # new_action.execute(self.kbucket)
            new_node = Node(int(payload[0]["data"]["id"]), payload[0]["data"]["ip"], int(payload[0]["data"]["port"]))
            self.kbucket.insert(new_node)
        elif cmd == "store":
            action = DoneStoring.from_payload_dict(sender, payload[0])
            action.execute(self.kbucket)

            