# File structure

The file structure has been designed to allow as much exstensibility as possible. Constants are generally contained in seperate files too.

## app/act

The place to define components that help the autonomous vehicle act. All components should obey the **Actuator** abstract base class. Current components include:

* **Accelerator** - a class representing an accelerate pedal.
* **Steering** - a class representing a steering reel.

## app/data/datastructures

The place to define datastructures used by components. Current datastructures include:

* **Fixed Array** - an array with a fixed length that cannot be easily changed. The main purpose of this datastructure is to hold I/O input data for a sensor components, replicating the physical memory. This datastructure is an educational tool, and could be replaced by moree efficent data structures such as a bytearray or numpy array.
* **Graph** - an unweighted graph, with integers as nodes. The main purpose of the graph is describe routes. Coordinates on a grid can be mapped to nodes, with edges of the graph representing roads between coordinates. Currently, Djikstra's shortet path algorithm is used to provide shortest path capabilities.
* **Package** -  an array split into two parts: one part for metadata, and the other part for data. The main purpose of a packet to to be a shared medium for data transfer between different components. Packages replicate internet communication packets. Furthermore, this data structure is handled by server compnents in the autonomous car.

## app/helperfunctions

The place to define functions useful in different files. Current helper functions include:

* **Type Converters** - for converting data between types. This is mainly used for converting binary data from sensor components into cartesian coordinates for planner components.
* **Guards** - for making explicit any paramater constraints on methods in classes.

## app/imports

The place to add any imports required by the main and testing scripts.

Special files named ***context.py*** are found throughout the folders, which are used to add the appropiate paths required to the system, for importing functions and classes into the main and testing scripts, irrespective of the folder structure. Those files point towards the import folder for convenience, so it would be wise to make sure all other modules for imports are included in the import folder. Current import files include: *

* ***components.py*** - module for all components
* ***datastructures*** - module all datastructures
* ***models.py*** - module for conceptual model classes

Special files named ***__init__.py*** files are also found within every folder, which are required to turn folders into packages to import from.
Therefore the import folder doesn't strictly need to be used, but it helps with code organisation. 

## app/network

The place to define network components of the autonomous vehicle, along with network config files.

Every vehicle component is classified as either a sensor, planner or actuator component, and cach class of component comes with a special **Server** that handles communication for that component with other components. These do the following:

* They convert data into packets and vice versa, facilitating data flow
* They send packets in a request-response manner
* The three types of server are : **SensorServer**, **PlannerServer**, **ActuatorServer**

Currently, the configuration involves:

* BASIC protocol - a format for packages, that derives from the User Datagram Protocol (UDP) of the internet protocol suite. The main difference is that UDP packets include a checksum, while a BASIC package includes an opcode instead. This protocol is a matter of convenience for early protyping,
and should be replaced by globally recognised protocols in the future to provide IoT capabilities.
* Address limitiations - a range of possible addresses is assigned to each component class. Assigned addresses can be updated using the globally accesible file, ***addresses.py***. In future versions, network switches and routers could provide distributed access, instead of the centralised approach currently used. The current implmentation is a matter of convenience for protyping.
* Synchronous network communication.

## app/plan

The place to define components that help the autonomous vehicle plan. All components should obey the **Planner** abstract base class. Current components include:

* **Mapper** - A component for localisation and route planning. A mapper object creates a **Map** object, which holds information about the road network.

A map is essentially a spanning tree and a n array, with geometrical correspondence between the two. The spanning tree is created using Kruskal's algorithm which is simple to implement and good enough for testing the software set up conceptually. This is not the most efficient algorithm though.

* **Navigator** - A component for managing car orientation. It's able to get the current orientation from a compass, compute a target orienation from information provided by a ampper, and instruct the steering wheel to steer. Future versions will take track acceleation too.

## app/sense

The place to define components that help the autonomous vehicle sense. All components should obey the **Sensorr** abstract base class. Current components include:

* **Compass** - a class encapsulating a compass.
* **Destination** - a class encapsulating a target destination request through UI.
* **GPS** - a class representing a global positioning system.

## app/ui

The place to put ui helper functions or classes.

Currently, the only file included is the **tui.py** file providing text-based ui convenience functions. Later versions could encapsulate the tui in it's own class, to facilitate the storage of user information.

## docs

The place to put documentation about the software

## tests/integration

The place to put tests of subsystems of components that are interacting.

## test/unit

The palce to put tests for individual classes.
