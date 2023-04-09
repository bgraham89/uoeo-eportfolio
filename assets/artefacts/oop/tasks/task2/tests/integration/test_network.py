'''Integration tests for network communication.'''

from context import (
    addresses as netid,
    components as avc,
    converters as conv,
    protocols
)
import unittest

class TestLocalisation(unittest.TestCase):
    '''Test that network communication facilitates localisation.'''

    def setUp(self):
        avc.SensorServer.id = netid.SENSE_MIN
        avc.PlannerServer.id = netid.PLAN_MIN

        self.data_size = 6
        self.map_width = self.map_height = 8
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

class TestDestination(unittest.TestCase):
    '''Test that network communication facilitates getting destination.'''

    def setUp(self):
        avc.SensorServer.id = netid.SENSE_MIN
        avc.PlannerServer.id = netid.PLAN_MIN

        self.data_size = 6
        self.map_width = self.map_height = 8
        self.destination = avc.Destination(self.data_size)
        self.mapper = avc.Mapper.WithRandomMap(self.map_width, self.map_height)
        self.destination_server = avc.SensorServer(self.destination)
        self.mapper_server = avc.PlannerServer(self.mapper)

    def test_netid_assignments(self):
        '''Expect assignments dict to be updated.'''
        self.assertEqual(netid.assignments[self.destination._key], self.destination_server)
        self.assertEqual(netid.assignments[self.mapper._key], self.mapper_server)

    def test_netid_servers(self):
        '''Expect assignments dict to be updated.'''
        self.assertEqual(netid.servers[self.destination_server._id], self.destination_server)
        self.assertEqual(netid.servers[self.mapper_server._id], self.mapper_server)

    def test_netid_idenities(self):
        '''Expect assignments dict to be updated.'''
        self.assertEqual(netid.identities[self.destination_server._id], self.destination._key)
        self.assertEqual(netid.identities[self.mapper_server._id], self.mapper._key)

    def test_request_sent_to_destination(self):
        '''Expect destination_server to receive request'''
        self.destination.fake_data()
        self.mapper.request_target_location()
        self.mapper_server.make_request()
        self.mapper_server.send_packages()
        self.assertTrue(len(self.destination_server._incoming_packages) == 1)

    def test_response_received_from_destination(self):
        '''Expect mapper_server to receive response'''
        self.destination.fake_data()
        self.mapper.request_target_location()
        self.mapper_server.make_request()
        self.mapper_server.send_packages()
        self.destination_server.open_packages()
        self.assertTrue(len(self.mapper_server._incoming_packages) == 1)

    def test_response_from_destination_is_readable(self):
        '''Expect mapper to receive correct coords'''
        self.destination.fake_data()
        self.mapper.request_target_location()
        self.mapper_server.make_request()
        self.mapper_server.send_packages()
        self.destination_server.open_packages()
        self.mapper_server.open_packages()
        destination_int = conv.array_to_int(self.destination.read_data())
        destination_coords = conv.int_to_coord(destination_int, self.map_width, self.map_height)
        self.assertEqual(self.mapper._target_location, destination_coords)

class TestMapper(unittest.TestCase):
    '''Test that network communication facilitates getting coords.'''

    def setUp(self):
        avc.SensorServer.id = netid.SENSE_MIN
        avc.PlannerServer.id = netid.PLAN_MIN

        self.data_size = 6
        self.map_width = self.map_height = 8
        self.gps = avc.GPS(self.data_size)
        self.destination = avc.Destination(self.data_size)
        self.mapper = avc.Mapper.WithRandomMap(self.map_width, self.map_height)
        self.gps_server = avc.SensorServer(self.gps)
        self.destination_server = avc.SensorServer(self.destination)
        self.mapper_server = avc.PlannerServer(self.mapper)

    def test_multiple_request_reponses(self):
        '''Expect mapper to recieve all information.'''
        self.gps.fake_data()
        self.destination.fake_data()
        self.mapper.request_current_location()
        self.mapper.request_target_location()
        self.mapper_server.make_request()
        self.mapper_server.send_packages()
        self.gps_server.open_packages()
        self.destination_server.open_packages()
        self.mapper_server.open_packages()
        gps_int = conv.array_to_int(self.gps.read_data())
        gps_coords = conv.int_to_coord(gps_int, self.map_width, self.map_height)
        self.assertEqual(self.mapper._current_location, gps_coords)
        destination_int = conv.array_to_int(self.destination.read_data())
        destination_coords = conv.int_to_coord(destination_int, self.map_width, self.map_height)
        self.assertEqual(self.mapper._target_location, destination_coords)

class TestOrientation(unittest.TestCase):
    '''Test that network communication facilitates getting orientation.'''

    def setUp(self):
        avc.SensorServer.id = netid.SENSE_MIN
        avc.PlannerServer.id = netid.PLAN_MIN

        self.compass_size = 2
        self.coord_size = 6
        self.map_size = 8

        # create components
        self.compass = avc.Compass(self.compass_size)
        self.gps = avc.GPS(self.coord_size)
        self.destination = avc.Destination(self.coord_size)
        self.navigator = avc.Navigator()
        self.mapper = avc.Mapper.WithRandomMap(self.map_size, self.map_size)
        self.compass_server = avc.SensorServer(self.compass)
        self.gps_server = avc.SensorServer(self.gps)
        self.destination_server = avc.SensorServer(self.destination)
        self.navigator_server = avc.PlannerServer(self.navigator)
        self.mapper_server = avc.PlannerServer(self.mapper)

        # populate mapper
        self.gps.fake_data()
        self.destination.fake_data()
        self.mapper.request_current_location()
        self.mapper.request_target_location()
        self.mapper_server.make_request()
        self.mapper_server.send_packages()
        self.gps_server.open_packages()
        self.destination_server.open_packages()
        self.mapper_server.open_packages()

    def test_netid_assignments(self):
        '''Expect assignments dict to be updated.'''
        self.assertEqual(netid.assignments[self.compass._key], self.compass_server)
        self.assertEqual(netid.assignments[self.navigator._key], self.navigator_server)

    def test_netid_servers(self):
        '''Expect assignments dict to be updated.'''
        self.assertEqual(netid.servers[self.compass_server._id], self.compass_server)
        self.assertEqual(netid.servers[self.navigator_server._id], self.navigator_server)

    def test_netid_idenities(self):
        '''Expect assignments dict to be updated.'''
        self.assertEqual(netid.identities[self.compass_server._id], self.compass._key)
        self.assertEqual(netid.identities[self.navigator_server._id], self.navigator._key)

    def test_request_sent_to_compass(self):
        '''Expect compass_server to receive request'''
        self.compass.fake_data()
        self.navigator.request_current_orientation()
        self.navigator_server.make_request()
        self.navigator_server.send_packages()
        self.assertTrue(len(self.compass_server._incoming_packages) == 1)

    def test_response_received_from_compass(self):
        '''Expect navigator_server to receive response'''
        self.compass.fake_data()
        self.navigator.request_current_orientation()
        self.navigator_server.make_request()
        self.navigator_server.send_packages()
        self.compass_server.open_packages()
        self.assertTrue(len(self.navigator_server._incoming_packages) == 1)

    def test_response_from_compass_is_readable(self):
        '''Expect navigator to receive correct coords'''
        self.compass.fake_data()
        self.navigator.request_current_orientation()
        self.navigator_server.make_request()
        self.navigator_server.send_packages()
        self.compass_server.open_packages()
        self.navigator_server.open_packages()
        compass_int = conv.array_to_int(self.compass.read_data())
        compass_direction = self.navigator._directions[compass_int]
        self.assertEqual(self.navigator._current_orientation, compass_direction)

    def test_request_sent_to_mapper(self):
        '''Expect mapper_server to receive request'''
        self.mapper.plan()
        self.navigator.request_target_orientation()
        self.navigator_server.make_request()
        self.navigator_server.send_packages()
        self.assertTrue(len(self.mapper_server._incoming_packages) == 1)

    def test_response_received_from_mappers(self):
        '''Expect navigator_server to receive response'''
        self.mapper.plan()
        self.navigator.request_target_orientation()
        self.navigator_server.make_request()
        self.navigator_server.send_packages()
        self.mapper_server.open_packages()
        self.assertTrue(len(self.navigator_server._incoming_packages) == 1)

    def test_response_from_mapper_is_readable(self):
        '''Expect navigator to receive correct direction'''
        self.mapper.plan()
        self.navigator.request_target_orientation()
        self.navigator_server.make_request()
        self.navigator_server.send_packages()
        self.mapper_server.open_packages()
        self.navigator_server.open_packages()
        mapper_int = self.mapper._plan[1] - self.mapper._plan[0]
        if mapper_int == 1:
            next_direction = "East"
        elif mapper_int == - 1:
            next_direction = "West"
        elif mapper_int > 1:
            next_direction = "North"
        else:
            next_direction = "South"
        self.assertEqual(self.navigator._target_orientation, next_direction)

if __name__ == '__main__':
    unittest.main()