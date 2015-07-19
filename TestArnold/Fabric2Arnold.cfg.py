#
# This config file defines the various options
# and overrides for converting a C++ API to KL
# The output files are intended to be consumed
# by kl2edk utility
#

cppToKLTypeMapping = {
    'unsigned int': 'UInt32',
    'int': 'SInt32',
    'float': 'Float32',
    'double': 'Float64',
    'long long': 'SInt64',
    'bool': 'Boolean',
    'UINT': 'UInt32',
    'void*': 'Data',
    'void': '',
    'char*': 'String',

    'AtByte' : 'UInt8',
    'AtBBox': 'Box3',
    'AtRGB': 'RGB',
    'AtColor': 'Vec3',
    'AtRGBA': 'Color',
    'AtEnum': 'String[]',
    'AtUInt16' : 'UInt16',
    'AtUInt32' : 'UInt32',
    'AtUInt64' : 'UInt64',
    'AtString' : 'String',
    'AtPoint' : 'Vec3',
    'AtVector' : 'Vec3',
    'AtPoint2' : 'Vec2',
    'AtVector2' : 'Vec2',
    'AtMatrix' : 'Mat44',
    'AtBucket': 'Data',
    'AtList' : 'Data'
}

# Name of this project
project_name = 'Fabric2Arnold'
# Specify the root of the doxygen output directory.  This dir is relative to this file
xml_dir = '../DoxygenXML/xml/'
# Specify where the output files are written.  This dir is relative to this file
output_dir = 'GenKL'

filesToProcess = [
    'ai_params.h',
    "ai_cameras.h",
    'ai_dotass.h',
    "ai_enum.h",
    "ai_license.h",
    'ai_metadata.h',
    'ai_msg.h',
    'ai_node_entry.h',
    'ai_nodes.h',
    'ai_render.h',
    'ai_plugins.h',
    'ai_ray.h',
    'ai_texture.h',
    'ai_universe.h'
]

# Any elements named in this list will not be exported
elementsToIgnore = [
    'AtCameraNodeMethods',
    'AiMsgSetCallback',
    'AtCommonMethods',
    'AtNodeMethods'
]

# Add extensions to be required.  Should
# this be per-file?  Or common for the whole project?
extns_required = [
    'Math'
]

# Add custom code to be added to the head of a file.
# It is possible to override built in translations by
# ignoring an element, and defining it explicitly here.
custom_add_to_file = {
    'ai_node_entry.h' : 'struct AtNodeEntry {\n'
                        '  Data internal;\n'
                        '};\n'
                        '\n'
                        'struct AtNodeMethods {\n'
                        '  Data internal;\n'
                        '};\n'
                        '\n'
                         'struct AtParamIterator {\n'
                        '  Data internal;\n'
                        '};\n'
                        '\n'
                        'struct AtMetaDataIterator {\n'
                        '  Data internal;\n'
                        '};\n\n',

    'ai_nodes.h' :      '// This represents a node in Arnold\n'
                        'struct AtNode {\n'
                        '  Data internal;\n'
                        '};\n\n'
                        'struct AtUserParamIterator {\n'
                        '  Data internal;\n'
                        '};\n\n',

    'ai_texture.h' :    'struct AtTextureHandle {\n'
                        '  Data handle;\n'
                        '};\n\n',

    'ai_ray.h' :        'struct AtShaderGlobals {\n'
                        '  Data handle;\n'
                        '};\n\n'
                        'struct AtScrSample {\n'
                        '  Data handle;\n'
                        '};\n\n',

    'ai_universe.h' :   'struct AtNodeIterator {\n'
                        '  Data iterator;\n'
                        '};\n'
                        '\n'
                        'struct AtNodeEntryIterator {\n'
                        '  Data iterator;\n'
                        '};\n'
                        '\n'
                        'struct AtAOVIterator {\n'
                        '  Data iterator;\n'
                        '};\n\n',

    'ai_params.h' :     'struct AtParamValue {\n'
                        '  Data atParamValue;\n'
                        '};\n'
                        '\n'
                        'UInt8 AtParamValue.asUInt8() = "_fe_AtParamValueAsUInt8";\n'
                        'UInt32 AtParamValue.asUInt32() = "_fe_AtParamValueAsUInt32";\n'
                        'Float32 AtParamValue.asFloat32() = "_fe_AtParamValueAsFloat32";\n'
                        'Vec3 AtParamValue.asVec3() = "_fe_AtParamValueAsVec3";\n'
                        'Mat44 AtParamValue.asMat44() = "_fe_AtParamValueAsMat44";\n'
                        'String AtParamValue.asString() = "_fe_AtParamValueAsString";\n'
                        '\n'
                        'struct AtArray {\n'
                        '  Data atParamValue;\n'
                        '};\n'
                        '\n'
                        'UInt8[] AtArray.asUInt8() = "_fe_AtArrayAsUInt8";\n'
                        'UInt32[] AtArray.asUInt32() = "_fe_AtArrayAsUInt32";\n'
                        'Float32[] AtArray.asFloat32() = "_fe_AtArrayAsFloat32";\n'
                        'Vec3[] AtArray.asVec3() = "_fe_AtArrayAsVec3";\n'
                        'Mat44[] AtArray.asMat44() = "_fe_AtArrayAsMat44";\n'
                        'String[] AtArray.asString() = "_fe_AtArrayAsString";\n'
                        '\n'
                        'struct AtParamEntry {\n'

                        '  Data handle;\n'
                        '};\n'
                        '\n'
                        'struct AtUserParamEntry {\n'
                        '  Data handle;\n'
                        '};\n'
                        '\n',

    'ai_metadata.h' :   'struct AtMetaDataStore {\n'
                        '  Data handle;\n'
                        '};\n\n',
}
# Define this value to true to not expose inline functions
skipInlineFunctions = True

#####
# The following parameters deal with creating a codegen file

# Specify a file to be merged with the auto-generated codegen file
# Items in this file will override the auto-generated items
# This file should be specified relative to this file
merge_codegen_file = "Fabric2Arnold.codegen.json"

# The parameter prefix is used to fill in the auto-generated
# codegen.json file.  It is required to auto-generate function bodies
parameter_prefix = 'f2a'
