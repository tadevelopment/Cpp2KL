
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

    'AtArray': 'TODOArray',
    'AtByte' : 'UInt8',
    'AtBBox': 'BBox',
    'AtRGB': 'Vec3',
    'AtColor': 'Vec3',
    'AtRGBA': 'Vec4',
    'AtEnum': 'String[]',
    'AtUInt16' : 'UInt16',
    'AtUInt32' : 'UInt32',
    'AtUInt64' : 'UInt64',
    'AtString' : 'String',
    'AtPoint' : 'Vec3',
    'AtVector' : 'Vec3',
    'AtPoint2' : 'Vec2',
    'AtVector2' : 'Vec2',
    'AtBucket': 'Data',
    'AtList' : 'Data'
}

# Name of this project
project_name = 'Fabric2Arnold'
# Specify the root of the doxygen output directory
xmlRootDir = './DoxygenXML/xml/'
# Specify where the output files are written: NOTE - this dir must exist
outputRootDir = 'E:/dev/OpusTech/Cpp2KL/GenKL/'

filesToProcess = [
    "ai_cameras.h",
    'ai_dotass.h',
    "ai_enum.h",
    "ai_license.h",
    'ai_metadata.h',
    'ai_msg.h',
    'ai_node_entry.h',
    'ai_nodes.h',
    'ai_render.h',
    'ai_params.h',
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

# Add custom code to be added to the head of a file.
# It is possible to override built in translations by
# ignoring an element, and defining it explicitly here.
custom_add_to_file = {
    'ai_node_entry.h' : 'struct AtNodeEntry {\n'
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
                        '};\n\n',

    'ai_texture.h' :    'struct AtTextureHandle {\n'
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
                        'UInt8 AtParamValue.asUInt8() = "_fe_AtParamValueAsUInt8"\n'
                        'UInt32 AtParamValue.asUInt32() = "_fe_AtParamValueAsUInt32"\n'
                        'Float32 AtParamValue.asFloat32() = "_fe_AtParamValueAsFloat32"\n'
                        'Vec3 AtParamValue.asVec3() = "_fe_AtParamValueAsVec3"\n'
                        'Mat44 AtParamValue.asMat44() = "_fe_AtParamValueAsMat44"\n'
                        'String AtParamValue.asString() = "_fe_AtParamValueAsString"\n'
                        '\n'
                        'struct AtParamEntry {\n'
                        '  Data handle;\n'
                        '};\n'
                        '\n'
                        'struct AtUserParamEntry {\n'
                        '  Data handle;\n'
                        '};\n'
                        '\n'
}
# Define this value to true to not expose inline functions
skipInlineFunctions = True
