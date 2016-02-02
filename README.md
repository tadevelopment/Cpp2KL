# Cpp2KL
This project automates the creation of Fabric extensions from C++ APIs.

USAGE:

Part 1 : C++ to XML

The Cpp2KL relies on the parsed output of C++ headers by Doxygen.

First, if not done already, download and install doxygen:
  www.doxygen.org/

Once installed, create/modify the sample doxygen script to generate output from the target API.  You will need to modify at least 3 doyxgen variables:
  PROJECT_NAME - Set to the name of your project
  OUTPUT_DIRECTORY - Set to the directory you Doxygen to send its Xml to
  INPUT - The 'include' directory of the API being wrapped

Run Doxygen with the your config script to generate Xml.

There are many other options in a full doxygen file, if the output files have problematic data, check the the full Doxygen documentation to see if there is anything in the options to help generate consumable output.

Part 2 : XML to KL

In order to convert, the tool needs some basic information about the API being parsed.  All supported options are detailed by Defaults.cfg.py.  Do not modify this file, instead create a new py file on your project directory to define your own parameters.  The defaults will always be loaded, and the project-specific config will be evaluated next.  In this way, some semi-sane defaults exist, but can be modified by any project-specific options.

Next, run build.py with the path to the projects config path specified.  If you are very very lucky, the output will convert automatically to KL.  Most likely, you will need to manually define conversions of types from the API's C++ types to KL-appropriate types.

SAMPLES:

The most complete sample is the wrapping of the Arnold API:
https://github.com/tadevelopment/fabric2arnold

This is a good place to check out a sample Doxygen config file and Cpp2KL config.py.

DEPENDENCIES:

We depend on the output of Doxygen and a valid setup of Fabric Engine.  Before running the project the environment from Fabric should loaded using prompt.bat

SUPPORTED OS:

This project has beeen used on Windows & Linux/

SUPPORT:

If you run into any issues, contact me at stephen@tadevelopment.works
