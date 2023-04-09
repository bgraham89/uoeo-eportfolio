'''Designates range of addresses for different network components'''

SENSE_MIN = 1
SENSE_MAX = 32
PLAN_MIN = 33
PLAN_MAX = 64
ACT_MIN = 65
ACT_MAX = 96

SENSORS = ("GPS", "Destination", "Compass")
PLANNERS = ("Mapper", "Navigator")
ACTUATORS = ("Steering")

#  Servers associated with component keys
assignments = {
    "GPS" : None,
    "Destination" : None,
    "Compass": None,
    "Mapper" : None,
    "Navigator" : None,
    "Steering" : None
}

#  component keys associated with addresses
identities = {

}

#  Servers objects associated with addresses
servers = {

}