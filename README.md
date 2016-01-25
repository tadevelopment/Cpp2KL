# Cpp2KL
This project automates the creation of Fabric extensions from C++ APIs.

USAGE:

First, parse the C++ API using Doxygen.  A sample doxycfg will be provided at some point

In order to convert, the tool needs some basic information about the API being parsed.  All supported options are detailed Defaults.cfg.py.
Do not modify this file, instead create a new py file to overwrite-extend any necessary parameters.  The defaults will be be loaded, and the project-specific config will be evaluated next to.

Next, run build.py with the path to the projects config path specified.

DEPENDENCIES:

We depend on the output of Doxygen and a valid setup of Fabric Engine.  Before running the project the environment from Fabric should loaded using prompt.bat

SUPPORTED OS:

This project has beeen used on Windows & Linux/

SUPPORT:

If you run into any issues, contact me at stephen@tadevelopment.works
