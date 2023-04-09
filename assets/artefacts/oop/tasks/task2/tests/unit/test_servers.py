'''Unit tests for server components'''

from context import (
    addresses,
    components as avc,
    datastructures as avds,
    protocols
)
import unittest

class TestSensorServer(unittest.TestCase):
    '''Unit tests for the SensorServer class.'''

    def setUp(self):
        self.size = 8
        self.data = avds.FixedArray(160).update(["d", "u", "m", "m", "y", " ", "d", "a", "t", "a"] * 16)
        self.sensors = [avc.GPS(8) for _ in range(33)]
        self.op = protocols.Basic.OP["response"]
        self.target_address = 10
        
        avc.SensorServer.id = addresses.SENSE_MIN
    
    def test_unique_ids(self):
        '''Expect each server to have a different id.'''
        servers = [avc.SensorServer(sensor) for sensor in self.sensors[:2]]
        self.assertTrue(servers[0]._id != servers[1]._id)

    def test_limit_on_number_of_servers(self):
        '''Expect amount of servers is capped.'''
        with self.assertRaises(AssertionError):
            [avc.SensorServer(sensor) for sensor in self.sensors[:33]]

    def test_packages_made(self):
        '''Expect packages made and stored.'''
        sensor = self.sensors[0]
        server = avc.SensorServer(sensor)
        server.make_packages(self.data, self.op, self.target_address)
        self.assertTrue(len(server._outgoing_packages) == 5)
    
    def test_op_assigned_to_package(self):
        '''Expect op assigned correctly to package.'''
        sensor = self.sensors[0]
        server = avc.SensorServer(sensor)
        server.make_packages(self.data, self.op, self.target_address)
        package = server._outgoing_packages.pop()
        op = server.read_op(package)
        self.assertTrue(op, self.op)

    def test_address_assigned_to_package(self):
        '''Expect address assigned correctly to package.'''
        sensor = self.sensors[0]
        server = avc.SensorServer(sensor)
        server.make_packages(self.data, self.op, self.target_address)
        package = server._outgoing_packages.pop()
        address = server.read_address(package)
        self.assertTrue(address, self.target_address)

    def test_address_swappable_to_id(self):
        '''Expect address of package updated'''
        sensor = self.sensors[0]
        server = avc.SensorServer(sensor)
        server.make_packages(self.data, self.op, self.target_address)
        package = server._outgoing_packages.pop()
        altered_package = server.swap_address(package)
        self.assertTrue(altered_package, server._id)

class TestPlannerServer(unittest.TestCase):
    '''Unit tests for the PlannerServer class.'''

    def setUp(self):
        self.size = 8
        self.data = avds.FixedArray(160).update(["d", "u", "m", "m", "y", " ", "d", "a", "t", "a"] * 16)
        self.planners = [avc.Mapper.WithRandomMap(self.size, self.size) for _ in range(33)]
        self.op = protocols.Basic.OP["response"]
        self.target_address = 10
        
        avc.PlannerServer.id = addresses.PLAN_MIN
    
    def test_unique_ids(self):
        '''Expect each server to have a different id.'''
        planners = [avc.PlannerServer(planner) for planner in self.planners[:2]]
        self.assertTrue(planners[0]._id != planners[1]._id)

    def test_limit_on_number_of_servers(self):
        '''Expect amount of servers is capped.'''
        with self.assertRaises(AssertionError):
            [avc.PlannerServer(planner) for planner in self.planners[:33]]

    def test_packages_made(self):
        '''Expect packages made and stored.'''
        planner = self.planners[0]
        server = avc.PlannerServer(planner)
        server.make_packages(self.data, self.op, self.target_address)
        self.assertTrue(len(server._outgoing_packages) == 5)
    
    def test_op_assigned_to_package(self):
        '''Expect op assigned correctly to package.'''
        planner = self.planners[0]
        server = avc.PlannerServer(planner)
        server.make_packages(self.data, self.op, self.target_address)
        package = server._outgoing_packages.pop()
        op = server.read_op(package)
        self.assertTrue(op, self.op)

    def test_address_assigned_to_package(self):
        '''Expect address assigned correctly to package.'''
        planner = self.planners[0]
        server = avc.PlannerServer(planner)
        server.make_packages(self.data, self.op, self.target_address)
        package = server._outgoing_packages.pop()
        address = server.read_address(package)
        self.assertTrue(address, self.target_address)

    def test_sequence_assigned_to_package(self):
        '''Expect address assigned correctly to package.'''
        planner = self.planners[0]
        server = avc.PlannerServer(planner)
        server.make_packages(self.data, self.op, self.target_address)
        package = server._outgoing_packages.pop()
        sequence = server.read_sequence(package)
        self.assertTrue(sequence[0] == 1 and sequence[1] == 5)

    def test_address_swappable_to_id(self):
        '''Expect address of package updated'''
        planner = self.planners[0]
        server = avc.PlannerServer(planner)
        server.make_packages(self.data, self.op, self.target_address)
        package = server._outgoing_packages.pop()
        altered_package = server.swap_address(package)
        self.assertTrue(altered_package, server._id)

if __name__ == '__main__':
    unittest.main()