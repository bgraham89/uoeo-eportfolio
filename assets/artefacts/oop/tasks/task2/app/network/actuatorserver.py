#  class imports
from app.network.abstract.server import Server
from collections import deque

#  module imports
from app.helperfunctions import guards as guards
from app.network.config import addresses as netid

class ActuatorServer(Server):
    '''A server for a Actuator component.'''
    id = netid.ACT_MIN

    def __init__(self, actuator):
        self._actuator= actuator
        self._incoming_packages = deque()
        self._id = self.make_id()
        netid.servers[self._id] = self
        netid.assignments[self._actuator._key] = self
        netid.identities[self._id] = self._actuator._key

    def make_packages(self):
        '''Creates package for network transportation.'''
        pass

    def send_packages(self):
        '''Sends package from outgoing queue.'''
        pass

    def open_packages(self):
        '''Deciphers package in incoming queue.'''
        if not len(self._incoming_packages):
            return True
        else:
            package = self._incoming_packages.pop()
            data = package.read_data()
            self._actuator.perform_action(data)
            self.open_packages()
        
    @classmethod
    def _id_constraints(self):
        '''Asserts good id is allocated.'''
        def min_id(x):
            return x >= netid.ACT_MIN
        def max_id(x):
            return x <= netid.ACT_MAX
        return lambda x : min_id(x) and max_id(x)
    
    @classmethod
    def make_id(cls):
        '''Provides good id.'''
        new_id = cls.id
        guards.arg_cond((new_id,), cls._id_constraints())
        cls.id += 1
        return new_id
