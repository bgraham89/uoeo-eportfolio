# README for main.py

## Brief Outline

Version 0.0.0.1 of Dionysus has now been released. A version control system
provides the ability to track changes to a project according to GitHub (2022), so this project
makes use of remote repositories, and documentation with each version.
The main.py contains a script that provides the user the ability to manage a food
inventory from the command line. It provides some of the features talked about in the plan,
and forms a basis for the others. The application is currently able to store non-relational
data, and provides a database management interface for a range of CRUD operations.
The main.py script requires python 3.6+ to be run. It can be run using the command
line, from the directory of the main.py file; using the command: ‘python main.py’ or ‘python3
main.py’ depending on whether you have python version 2 installed as well.
Once the application has started, the command line provides a text-based interface,
that can be interacted with using a keyboard. Prompts coordinate the database management
interface, and specify a range of inputs that can be used. Inputs are generally limited to 50
characters, and guardians are in place to ensure input is suitable for the occasion.
Note. A shortcut has been added where pressing ‘enter’ is interpreted as the key ‘y’,
during requests for a yes or no response.

## Features

Features of this version include:

* A non-relational database that’s built upon a hashmap, (and linked lists), and makes
use of the algorithms outlined previously. The algorithms have been slightly adjusted
to provide better functionality, yet remain implicitly identical.
* A database management system that bridges data structure operations to database
actions. Actions include creating, reading, updating and deleting data, as well as
searching, filtering and sorting data.
* A debug mode that enables console logs during database actions. Python (2022)
explains that logging provides a way to guarantee events have happened as
expected during a script. The implemented logs are helpful for big bang integration
testing.
* Docstrings on classes and methods for educational purposes. Inline comments have
been used to identify key steps in algorithms too.
* Demos for performance testing, that provide large amount of data to the database.
* An additional algorithm mentioned in the plan; to grow the size of the storage in the
hashmap dynamically. Whenever the storage is half full, it doubles in size, and all
data is then moved from its old address to a new address.

## Organisation

The main.py code has been organised into classes, following the object-oriented
paradigm. Guttag (2021) says that the use of classes is a modern approach to programming.
Benefits include the separation of components that are essential to the script, which
improves code-readability, and control over the programme, with the use of design patterns.
The structure of the code is separated as follows:

1. Standard library imports for timing and randomisation functions. Timing is
controlled to provide a calmer user experience to the application, while
randomisation is used to produce demos.
2. Global variables which includes one variable that controls debug mode, and is
required by all classes.
3. Data structures for the hashmap and node (linked list component) classes.
4. Assertion classes which are used by other classes to provide internal unit tests.
These ensure the state of parameters, inputs and other variables obey expected
constraints. Those constraints mainly consist of size and type constraints, but
also include experimental object constraints for the hashmap, for future
experimentation. Microsoft (2022) recommends using a unit testing framework to
create unit tests to verify behaviour, which the assertion classes are designed to
provide.
5. Strategy classes for the strategy object used during sorting-actions, separating
the hybrid algorithm from the hashmap class that implements them.
6. Database management classes which include an entity-based, non-relational
database class for database actions, and controls the interactions between user
interfaces and data structures.
7. User Interface classes which include a command-line interface class that
encapsulates text based input and output, and handles selections. Attention has
been given to user experience, with the use of politeness.
8. Test data which for procedurally generated test data.
9. Scripts which contain the main programme.

Other benefits of the object-oriented paradigm are the syntax freedoms that it provides
for implementing algorithms, and the freedoms for portraying objects.
A good interface should be easy to understand. The advantage of good syntax is for
developers and future development, so the code obeys Python’s (2001) PEP 8 style guide.
Limitations have prevented version 0.0.0.1 to take advantage of:

* A modular paradigm, that allows the separation of code into different files, for
distributed development and simpler code parsing.
* Python 3.10 which features the walrus operator and switch statements to reduce the
complexity of flow-control structures in algorithms.
* External libraries and API’s which provide state of the art natural language parsing,
data analysis and voice recognition capabilities, including the libraries NumPy,
TensorFlow and Google API’s.

## Quality Assurance

While the code contains methods of unit, integration and performance testing
outlined and planned above, feedback of this version will be valuable too. A sidenote too;
Version 0.0.0.1 doesn’t contain any asynchronous functions so no tests have made to check
that.

## References

Github (2022) About Git. Available from https://docs.github.com/en/get-started/using-
git/about-git [Accessed on 27/11/2022].

Guttag, J. (2021) Introduction to Computing and Programming Using Python. 3rd ed.
Massachusetts: The MIT Press. 179.

Microsoft (2022) Unit test basics. Available from https://learn.microsoft.com/en-
us/visualstudio/test/unit-test-basics?view=vs-2022 [Accessed on 27/11/2022].

Python (2001) Style Guide for Python code. Available from
https://peps.python.org/pep-0008/ [Accessed on 27/11/2022].

Python (2022) Logging HOWTO. Available from
https://docs.python.org/3/howto/logging.html#logging-basic-tutorial [Accessed on
27/11/2022].