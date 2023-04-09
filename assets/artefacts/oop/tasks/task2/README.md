# README

This code is an imitation autonomous car system. To understand how the software works, checkout the doc folder. The ***fille_structure.py*** file is especially important. The main programme is in the ***main.py*** script. The car can currently navigate itself, route plan, and drive.

## Set Up

This code requires python version 3.8+, so please double check that you have it.

To find out if python 3.8+ is installed on your machine, from the command line, type:

> python -version

If you dont have it installed, you can install it from [python.org](https://www.python.org/).

Once you have the correct version, you can run this programme, by making this folder your active directory, and then typing:

> python app/main.py

To run tests type either of the follwing:

> python/tests/unit/test_datastructures.py
> python/tests/unit/test_helperfunctions.py
> python/tests/unit/test_models.py
> python/tests/unit/test_planners.py
> python/tests/unit/test_sensors.py
> python/tests/unit/test_servers.py
> python/tests/integration/test_network.py