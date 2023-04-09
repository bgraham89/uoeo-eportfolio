'''Main programme'''

from context import (
    components as avc,
    converters as conv,
    models as avm,
    tui
)

class Main(object):
    '''The main programme for the autonomous car.'''

    def __init__(self):
        self.create_components()
        self.localise()

    def __call__(self):
        self.introduce_ai()
        while True:
            self.establish_destination()
            self.establish_route()
            self.drive_route()
            if not self.continue_driving():
                self.goodbye()
                break

    def create_components(self):
        '''Creates all the car components'''
        #  sensor system
        self.word_size = 6 #  2 log 2 of map size
        self.gps = avc.GPS(self.word_size) 
        self.gps_server = avc.SensorServer(self.gps)
        self.destination = avc.Destination(self.word_size)
        self.destination_server = avc.SensorServer(self.destination)
        self.compass = avc.Compass(2)
        self.compass_server = avc.SensorServer(self.compass)

        #  planner system
        self.map_size = 8
        self.mapper = avc.Mapper.WithRandomMap(self.map_size, self.map_size)
        self.mapper_server = avc.PlannerServer(self.mapper)
        self.navigator = avc.Navigator()
        self.navigator_server = avc.PlannerServer(self.navigator)
        self.locations = avm.make_road_names(self.map_size ** 2)

        # actuator system
        self.steering = avc.Steering()
        self.steering_server = avc.ActuatorServer(self.steering) 

    def localise(self, position = None):
        '''Gets the cars current position'''
        if not position:
            self.gps.fake_data()
        else:
            self.gps.write_data(position)
        self.mapper.request_current_location()
        self.mapper_server.make_request()
        self.mapper_server.send_packages()
        self.gps_server.open_packages()
        self.mapper_server.open_packages()

    def establish_destination(self):
        '''Establish a location to drive too.'''
        self.user_input_destination()
        self.mapper.request_target_location()
        self.mapper_server.make_request()
        self.mapper_server.send_packages()
        self.destination_server.open_packages()
        self.mapper_server.open_packages()

    def establish_route(self):
        '''Find the shortest path from current location'''
        if self.mapper._current_location == self.mapper._target_location:
            id = conv.coord_to_int(self.mapper._current_location, self.map_size)
            self.mapper._plan = [id]
        else:
            self.mapper.plan()
    
    def drive_route(self):
        '''Drives route.'''
        if len(self.mapper._plan) == 1:
            information = "We are already at your destination"
            tui.ux_print(information)
            return
        orientation = position = None
        while True:
            self.orientate(orientation) # parameter is temp necessity to update compass
            orientation = self.plan_turn() # assignment is temp necessity to update compass
            self.steer()
            position = self.accelerate() # assignment is temp necessity to update gps
            self.localise(position)  # paramater is temp necessity to update gps
            if len(self.mapper._plan) == 1:
                break
        information = "We have arrived at your destination"
        tui.ux_print(information)
        return
    
    def orientate(self, orientation = None):
        '''Gets the cars current orientation'''
        if not orientation:
            self.compass.fake_data()
        else:
            self.compass.write_data(orientation)
        self.navigator.request_current_orientation()
        self.navigator_server.make_request()
        self.navigator_server.send_packages()
        self.compass_server.open_packages()
        self.navigator_server.open_packages()

    def plan_turn(self):
        '''Gets information ready for actuators'''
        orientation = self.establish_target_orientation()
        self.navigator.plan()
        return orientation  # temp necessity to update compass
    
    def establish_target_orientation(self):
        '''Gets target orientation for vehicle.'''
        self.navigator.request_target_orientation()
        self.navigator_server.make_request()
        self.navigator_server.send_packages()
        self.mapper_server.open_packages()
        self.navigator_server.open_packages()
        direction = self.navigator._target_orientation
        direction_i = self.navigator._directions.index(direction)
        return conv.int_to_array(direction_i, 2)
    
    def steer(self):
        '''Changes cars orientation'''
        self.navigator_server.make_request()
        self.navigator_server.send_packages()
        if len(self.steering_server._incoming_packages):
            self.steering_server.open_packages()
        else:
            information = "The car continues straight on."
            tui.ux_print(information)

    def accelerate(self):
        '''Moves car forward.'''
        if self.mapper._plan: 
            self.update_route() 
            place = self.locations[self.mapper._plan[0]]
            information = f"The car is now at {place}."
            tui.ux_print(information, 1.5)
            return conv.int_to_array(self.mapper._plan[0], self.word_size)  #temp necessity to update gps

    def update_route(self):
        '''
        Update route.
        
        This method removes the first item from the route,
        as it's assumed this method is called upon entry
        of a coord. A more efificent way of doing this would
        be to use a pointer instead of mutating the route.

        '''
        self.mapper._plan = self.mapper._plan[1:]

        
    def introduce_ai(self):
        '''Greets the user and tries to get a name'''
        greetings = "Hi, I'm BradCar, welcome to this vehicle."
        tui.ux_print(greetings)
        current_loc_i = conv.coord_to_int(self.mapper._current_location, self.map_size)
        current_loc = self.locations[current_loc_i]
        information = f"I've been sat at {current_loc} for around 10 minutes now."
        tui.ux_print(information)
        prompt = "What's your name?\n"
        name = tui.get_string(prompt)
        greetings = f"Nice to meet you{' ' if name else ''}{name}. Let's work out where we're going."
        tui.ux_print(greetings)

    def user_input_destination(self):
        '''Get User Inputfor location'''
        prompt = "Do you need to see the options?"
        response = tui.get_bool(prompt)
        if response:
            information = f"I'm able to take you to any of the following places: "
            options = f"{self.locations}" 
            tui.ux_print(information)
            tui.ux_print(options)
        prompt = "Which place would you like to go?\n"
        choice = tui.get_choice(prompt, self.locations)
        if not choice:
            coords = self.mapper._current_location
            id = conv.coord_to_int(coords, self.map_size)
            choice = self.locations[id]
        else:
            id = self.locations.index(choice)
        data = conv.int_to_array(id, self.word_size)
        self.destination.write_data(data)
        information = f"Alrighty, we're on our way to {choice}. Get your belt on!"
        tui.ux_print(information)

    def continue_driving(self):
        '''Gives user a chance to go somewhere else'''
        prompt = "Would you like to go somewhere else?"
        response = tui.get_bool(prompt)
        return response
    
    def goodbye(self):
        '''Says goodby'''
        pleasentry = "Goodbye!"
        tui.ux_print(pleasentry)


if __name__ == '__main__':
    main = Main()
    main()