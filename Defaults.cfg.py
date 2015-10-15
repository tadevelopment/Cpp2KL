#
# This config file defines the various options
# and overrides for converting a C++ API to KL
# The output files are intended to be consumed
# by kl2edk utility
#


# Name of this project
project_name = 'ProjectNameNotSet'

# Specify the root of the doxygen output directory.  This dir is relative to this file
xml_dir = 'XmlDirNotSet'

# List all source (C++) files to convert to KL
filesToProcess = [
]

# Any elements named in this list will not be exported
elementsToIgnore = [
]

#
# A basic type mapping - each native argument
# encountered will be converted to the KL type
# 
cppToKLTypeMapping = {
    'unsigned int': 'UInt32',
    'int': 'SInt32',
    'float': 'Float32',
    'double': 'Float64',
    'long long': 'SInt64',
    'bool': 'Boolean',
    'boolean': 'Boolean',
    'UINT': 'UInt32',
    'void*': 'Data',
    'void': '',
    'char*': 'String',
}

# Some API's (thanks MS) have additional semantics written
# into them to describe how functino parameters are meant
# to be used.  If this info exists, we can attempt to infer
# the correct usage of a parameter (in, out, array etc)
# from these additional semantics
# see: https://msdn.microsoft.com/en-CA/library/hh916383.aspx
use_ms_sal = False

#
# When multiple C++ types map to a single KL
# type, it becomes impossible to correctly remap
# the conversion functions for the KL type back
# to the correct C++ type.  To resolve these 
# issues, we can create a KL 'alias' for the type
# which allows us to specify a unique KL type in the
# generated fn signatures, and this type lets us know
# the correct C++ type to convert to in the 
# kl2edk phase
# NOTE: The alias must be named the same as the C++ type
#
kl_alias_file_name = '_aliases'
kl_type_aliases = {
    'HRESULT' : 'UInt32'
}

# C-Style API's often use typedef's
# to name their types sanely, eg:
#   typedef enum _MyType MyType;
#   enum _MyType;
# We can use fabric's alias function
# to support the multiple names:
#   alias _MyType UInt32;
#   alias MyType _MyType;
convert_typedef_to_alias = True;

#
# If an SDK exposes opaque types (eg, handles) then
# the only interaction KL can have with these objects
# is to pass them around as Data pointers.  To maintain
# some type-safety, we can generate structs to wrap
# these pointers that simply contain a Data ptr. 
# Note - the opaque_file_name should not conflict
# with any filesToProcess, or it may be overwritten
#
opaque_file_name = '_opaque_types'
opaque_type_wrappers = [
]

#
# We need to define a list of KL POD types
# When generating the fn definition in kl2edk,
# complex (non-POD) types will be passed an IO
# parameter to set as a return value, while
# POD types will return their value directly.
# We need to know which is which in order to
# correctly generate the function implementations
#
kl_pod_types = [
    'UInt8',
    'SInt8',
    'UInt16',
    'SInt16',
    'UInt32',
    'SInt32',
    'UInt64',
    'SInt64',
    'Float32',
    'Float64',
    'Boolean',
    'Data'
]

# Specify where the output files are written.  This dir is 
# relative to cfg file supplied as an argument to build.py
output_dir = 'GenKL'
output_h_dir = 'GenCPP/h'
output_cpp_dir = 'GenCPP/cpp'

# specify where custom CPP files (if any) are located
custom_cpp_dir = 'CustomCPP'
# specify where custom KL files (if any) are located
custom_KL_dir = 'CustomKL'


# Add extensions to be required.  Should
# this be per-file?  Or common for the whole project?
extns_required = [
    'Util'
]

# Add custom code to be added to the head of a file.
# It is possible to override built in translations by
# ignoring an element, and defining it explicitly here.
custom_add_to_file = {
    'ExampleHeader.h' : '// This is some code\n'
                        '// That would be added to\n'
                        '// ExampleHeader.kl\n'
}

# Define this value to true to not expose inline functions
skipInlineFunctions = True

#####
# The following parameters deal with creating a codegen file

# Specify a file to be merged with the auto-generated codegen file
# Items in this file will override the auto-generated items
# This file should be specified relative to this file
merge_codegen_file = project_name + ".codegen.json"

# The parameter prefix is used to fill in the auto-generated
# codegen.json file.  It is required to auto-generate function bodies
parameter_prefix = 'cpp2kl'
