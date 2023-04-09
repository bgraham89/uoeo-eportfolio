#  class imports
from app.data.datastructures.package import Package
from app.network.abstract.server import Server
from app.network.config.protocols import Basic
from collections import deque

#  module imports
from app.helperfunctions import converters as conv, guards
from app.network.config import addresses as netid

class PlannerServer(Server):
    '''A server for a Planner component.'''
    id = netid.PLAN_MIN

    def __init__(self, planner):
        self._planner = planner
        self._outgoing_packages = deque()
        self._incoming_packages = deque()
        self._id = self.make_id()
        netid.servers[self._id] = self
        netid.assignments[self._planner._key] = self
        netid.identities[self._id] = self._planner._key

    def make_packages(self, data, op, address):
        '''Creates package for network transportation.'''
        body_size = Basic.BODY_SIZE
        num_packages = max(len(data) // body_size, 1)  #padding if no data
        for i in range(num_packages):
            meta_data = {
                "this" : i+1, 
                "last" : num_packages,
                "address" : address,
                "op" : op
            }
            data_i = i * body_size
            data_j = data_i + body_size
            data_slice = data[data_i:data_j]
            package = Package.Basic(data_slice, meta_data)
            self._outgoing_packages.appendleft(package)
    
    def make_request(self):
        if not len(self._planner._instructions):
            return True
        else:
            key, data = self._planner.give_instruction()
            address = netid.assignments[key]._id
            op = Basic.OP["request"]
            if not data:
                data = []
            self.make_packages(data, op, address)
            self.make_request()
        
    def send_packages(self):
        '''Sends package from outgoing queue.'''
        if not len(self._outgoing_packages):
            return True
        else:
            package = self._outgoing_packages.pop()
            dest_address = self.read_address(package)
            package_ready = self.swap_address(package)  #destination needs senders address
            server = netid.servers[dest_address]
            server._incoming_packages.appendleft(package_ready)
            self.send_packages()

    def open_packages(self):
        '''Deciphers package in incoming queue.'''
        if not len(self._incoming_packages):
            return True
        else:
            package = self._incoming_packages.pop()
            op = self.read_op(package)
            do_reply = op == Basic.OP["request"]
            if do_reply:
                address = self.read_address(package)
                self.send_reply_packages(address)
            else:
                self.collect_response(package)
            self.open_packages()
    
    def send_reply_packages(self, address):
        '''Send information as reply to request.'''
        id = netid.identities[address]
        data = self._planner.reply_with_information(id)
        op = Basic.OP["response"]
        self.make_packages(data, op, address)
        self.send_packages()

    def read_op(self, package):
        '''Get op from package (to determine next action).'''
        head = package.read_meta_data()
        op = conv.array_to_int(head[:Basic.HEAD_SEGMENT_SIZE])
        return op

    def read_address(self, package):
        '''Get senders address from package (to determine where to reply).'''
        head = package.read_meta_data()
        seg = Basic.HEAD_SEGMENT_SIZE
        address = conv.array_to_int(head[seg:2*seg])
        return address
    
    def read_sequence(self, package):
        '''Get sequence information from package (to determine where to reply).'''
        head = package.read_meta_data()
        seg = Basic.HEAD_SEGMENT_SIZE
        current = conv.array_to_int(head[2*seg:3*seg])
        final = conv.array_to_int(head[3*seg:4*seg])
        return current, final
    
    def swap_address(self, package):
        '''Swap the address stored in a package with the sensors address'''
        sender_address = conv.int_to_array(self._id, Basic.HEAD_SEGMENT_SIZE)
        package.update_address(sender_address)
        return package
    
    def collect_response(self, package):
        '''Opens a sequence of packages and gets all of the data.'''
        current, final = self.read_sequence(package)
        data = package.read_data()
        while current != final:
            package = self._incoming_packages.pop()
            current, __ = self.read_sequence(package)
            data.extend(package.read_data())
        address = self.read_address(package)
        op = netid.identities[address]
        self._planner.extract_information(op, data)

    @classmethod
    def _id_constraints(self):
        '''Asserts good id is allocated.'''
        def min_id(x):
            return x >= netid.PLAN_MIN
        def max_id(x):
            return x <= netid.PLAN_MAX
        return lambda x : min_id(x) and max_id(x)
    
    @classmethod
    def make_id(cls):
        '''Provides good id.'''
        new_id = cls.id
        guards.arg_cond((new_id,), cls._id_constraints())
        cls.id += 1
        return new_id
