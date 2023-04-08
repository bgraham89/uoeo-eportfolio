# File structure

## ./data/datastructures

The place to define datastructures. Custom data structures of this version include:

* **Fixed Array** - an array with a fixed length that cannot be easily changed. The main purpose of this datastructure is to serve as a I/O container for sensor components. It serves more as an educational tool, or proof of concept than as optimal structure. A more efficent data structure would be a bytearray or numpy array.
* **Graph** - an unweighted graph, with integers as nodes. Djikstra's shortet path algorithm is used to provide shortest path capabilities. The main purpose of the graph is describe routes available, by mapping nodes to coordinates on a grid.
* **Package** - essentially an array split into two: one part for metadata, the other part for data. A package is a protoype of packets used in low-level internet communication. The main purpose of a package is to provide a universal container for data sent between different components of an autonomous car. Each component is connected to a server that shapes data into packages to send to other servers, which in turn, shapes the packages to the benefit of dependent components. The specific structure of a package is a variant of the User Datagram Protocol (UDP) of the internet protocol suite. The checksum metadata of UDP is instead replaced by opcode metadata, as is most convenient in this prototype.

## ./helperfunctions

The place to define functions useful in different files. Custom helper functions of this version are:

* **Type Converters** - for converting data between types. This is mainly used for converting binary data from sensor components into cartesian coordinates for planner components.
* **Guards** - for making explicit any paramater constraints on methods in low level classes.

## ./imports

The place to add any imports required by the main and testing scripts. Special files named ***context.py*** are used to add the appropiate paths required to import functions and classes into the main script, and the testing scripts, that points to this folder. Special files named ***__init__.py*** files are required to turn folders into packages to import from.

## ./network

The place to define network components and network config files. Each component of the autonomous vehicle is classified as either a sensor, planner or actuator. Each component is assigned to a special **Server** that handles communication of the component with others, facilitating data flow. Each server implements the same abstract base class, but has subtle differences to each other. Further inheritence has been avoided so as not be too restrictive. The network makes use of synchronous network behaviour, but asynchronous behaviour would be better suited, and should be a goal of the next version. ***protocols.py*** provides configuration for the **Basic** protocol useed in this prototype network. ***addresses.py*** provides a global directory for network addresses, which would be better handled by network switches and routers in future versions. Most network communication currently follows a request-response pattern.

## ./plan

The place to define components that help the autonomous vehicle plan. They should obey the planner abstract base class. Components include:

* **Mapper** - for localisation and route planning. The mapper class depends upon a **Map** model. For the purpose of the prototype, a map is essentially a spanning tree upon a grid. The spanning tree is created using Kruskal's algorithm. This is not the most efficient algorithm, but is good enough for a prototype.

## ./sense

The place to define components that help the autonomous vehicle sense. They should obey the sensor abstract base class. Components include:

* **GPS** - a mock up of a global positioning systems
* **Destination** - a mock up of a UI Post containing a target destination.