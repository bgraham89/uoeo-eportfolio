'''Integration tests for network communication.'''

from context import addresses as netid
from context import components as avc
from context import converters as conv
from context import protocols
import unittest

class TestLocalisation(unittest.TestCase):
    '''Test that network communication facilitates localisation.'''

    def setUp(self):
        avc.SensorServer.id = netid.SENSE_MIN
        avc.PlannerServer.id = netid.PLAN_MIN

        self.data_size = protocols.Basic.BODY_SIZE
        self.map_width = self.map_height = self.data_size // 2
        self.gps = avc.GPS(self.data_size)
        self.mapper = avc.Mapper.WithRandomMap(self.map_width, self.map_height)
        self.gps_server = avc.SensorServer(self.gps)
        self.mapper_server = avc.PlannerServer(self.mapper)

    def test_netid_assignments(self):
        '''Expect assignments dict to be updated.'''
        self.assertEqual(netid.assignments[self.gps._key], self.gps_server)
        self.assertEqual(netid.assignments[self.mapper._key], self.mapper_server)

    def test_netid_servers(self):
        '''Expect assignments dict to be updated.'''
        self.assertEqual(netid.servers[self.gps_server._id], self.gps_server)
        self.assertEqual(netid.servers[self.mapper_server._id], self.mapper_server)

    def test_netid_idenities(self):
        '''Expect assignments dict to be updated.'''
        self.assertEqual(netid.identities[self.gps_server._id], self.gps._key)
        self.assertEqual(netid.identities[self.mapper_server._id], self.mapper._key)

    def test_request_sent_to_gps(self):
        '''Expect gps_server to receive request'''
        self.gps.fake_data()
        self.mapper.request_current_location()
        self.mapper_server.make_request()
        self.mapper_server.send_packages()
        self.assertTrue(len(self.gps_server._incoming_packages) == 1)

    def test_response_received_from_gps(self):
        '''Expect mapper_server to receive response'''
        self.gps.fake_data()
        self.mapper.request_current_location()
        self.mapper_server.make_request()
        self.mapper_server.send_packages()
        self.gps_server.open_packages()
        self.assertTrue(len(self.mapper_server._incoming_packages) == 1)

    def test_response_from_gps_is_readable(self):
        '''Expect mapper to receive correct coords'''
        self.gps.fake_data()
        self.mapper.request_current_location()
        self.mapper_server.make_request()
        self.mapper_server.send_packages()
        self.gps_server.open_packages()
        self.mapper_server.open_packages()
        gps_int = conv.array_to_int(self.gps.read_data())
        gps_coords = conv.int_to_coord(gps_int, self.map_width, self.map_height)
        self.assertEqual(self.mapper._current_location, gps_coords)

if __name__ == '__main__':
    unittest.main()