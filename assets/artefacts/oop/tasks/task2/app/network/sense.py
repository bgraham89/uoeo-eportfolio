import app.datastructures as avds
import app.helperfunctions.guards as guards
import app.helperfunctions.encoders as enc
import app.network.config.addresses as netid
from app.network.abstract.server import Server
from app.network.config.protocols import Basic
from collections import deque

class SensorServer(Server):
    '''A server for a Sensor component.'''
    id = 1

    def __init__(self, sensor):
        self._sensor = sensor
        self._outgoing_packages = deque()
        self._incoming_packages = deque()
        self._id = self.make_id()
        netid.assigned[self._id] = self

    def make_packages(self, data, op, address):
        '''Creates package for network transportation.'''
        body_size = Basic.BODY_SIZE
        num_packages = data // body_size
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
            package = avds.Package.Basic(data_slice, meta_data)
            self._outgoing_packages.appendleft(package)

    def send_packages(self):
        '''Sends package in outgoing queue.'''
        package = self._outgoing_packages.pop()
        if not package:
            return True
        else:
            dest_address = self.read_address(package)
            package_ready = self.swap_address(package)  #destination needs senders address
            device = netid.assigned[dest_address]
            device.incoming_packages.appendleft(package_ready)
            self.send_packages()

    def open_packages(self):
        '''Deciphers package in incoming queue.'''
        package = self._incoming_packages.pop()
        if not package:
            return True
        else:
            op = self.read_op(package)
            do_reply = op == Basic.OP["request"]
            do_reply and self.sendReply(package)
            self.open_packages()
    
    def send_reply_packages(self):
        '''Send sense data as reply to request package.'''
        op = Basic.OP["response"]
        data = self._sensor.read_memory()
        self.make_packages(data, op)
        self.send_packages()

    def read_op(self, package):
        '''Get op from package (to determine next action).'''
        head = package.read_meta_data()
        op = enc.array_to_int(head[:Basic.HEAD_SEGMENT_SIZE])
        return op

    def read_address(self, package):
        '''Get senders address from package.'''
        head = package.read_meta_data()
        seg = Basic.HEAD_SEGMENT_SIZE
        address = enc.array_to_int(head[seg:2*seg])
        return address
    
    def swap_address(self, package):
        '''Swap the address stored in a package with the sensors address'''
        sender_address = enc.int_to_array(self._id, Basic.HEAD_SEGMENT_SIZE)
        package.update_address(sender_address)
        return package
        
    @classmethod
    def _id_constraints(self):
        '''Asserts good id is allocated.'''
        def min_id(x):
            return x >= netid.SENSE_MIN
        def max_id(x):
            return x <= netid.SENSE_MAX
        return lambda x : min_id(x) and max_id(x)
    
    @classmethod
    def make_id(cls):
        '''Provides good id.'''
        new_id = cls.id
        guards.arg_cond((new_id,), cls._id_constraints())
        cls.id += 1
        return new_id
