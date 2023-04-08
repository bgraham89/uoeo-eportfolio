'''Designates range of addresses for different network components'''

SENSE_MIN = 1
SENSE_MAX = 32
PLAN_MIN = 33
PLAN_MAX = 64

SENSORS = ("GPS", "Destination")
PLANNER = ("Mapper")

#  Servers associated with component keys
assignments = {
    "GPS" : None,
    "Destination" : None,
    "Mapper" : None
}

#  component keys associated with addresses
identities = {

}

#  Servers objects associated with addresses
servers = {

}