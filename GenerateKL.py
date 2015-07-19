from __future__ import nested_scopes
import xml.etree.ElementTree as ET
import re
import os
import sys

#cfg_file_name = input('Enter config file name : folder/___.cfg.py ')
#pmName = "Fabric2Arnold.cfg.py"

if not len(sys.argv) > 1:
    print ("Usage - please pass the config file as an argument to this script")

# import the configuration file.
execfile(sys.argv[1])

def is_int(str):
    try:
        int(str, 0)
        return 1
    except ValueError:
        return 0
    except TypeError:
        return 0


def is_float(str):
    try:
        float(str)
        return 1
    except ValueError:
        return 0
    except TypeError:
        return 0


def get_str(node):
    if node == None:
        return ''
    res = ET.tostring(node, encoding="us-ascii", method="xml")
    # first, convert para nodes to new lines,
    res = ' '.join(res.split())
    res = res.replace('<para>', '')
    res = res.replace('</para>', '\n')
    res = ET.tostring(ET.XML(res), encoding="us-ascii", method="text")
    #res = ET.tostring(node, encoding="us-ascii", method="text")
    return res

def process_define(defineNode):
    # Write out an equivalent define to the output file
    name = defineNode.find('name').text
    value = defineNode.find('initializer')
    if (value == None):
        return ''

    if (name in elementsToIgnore):
        return ''

    value = value.text
    comment = get_str(defineNode.find('detaileddescription'))
    comment = comment.replace('\n', '')

    if (is_int(value)):
        klLine = "const Integer " + name + ' = ' + value + ';\t // ' + comment
        print(klLine)
        return klLine + '\n'

    elif (is_float(value)):
        klLine = "const Float32 " + name + ' = ' + value + ';\t // ' + comment
        print(klLine)
        return klLine + '\n'

    return ''


# Create a regular expression  from the dictionary keys
s_rex = re.compile(r"(\b%s(?=\Z|\s|\*|\&))" % r"(?=\Z|\s|\*|\&)|\b".join(map(re.escape, cppToKLTypeMapping.keys())))
def cpp_to_kl_type(cpp_arg_type, apply_io=False, args_str=None):
    # Now compact any pointer declarations, so that char * becomes char*
    # We maintain these values as part of the type mainly to differentiat char* from char
    kl_type = cpp_arg_type.replace(" *", "*")
    # Just remove &, as it does not change type
    kl_type = kl_type.replace("&", "")
    # convert to the KL version of this type
    str = r"(\b%s(?=\Z|\s|\*|\&))" % r"(?=\Z|\s|\*|\&)|\b".join(map(re.escape, cppToKLTypeMapping.keys()))
    sub_type = s_rex.sub(lambda mo: cppToKLTypeMapping[mo.string[mo.start():mo.end()]], kl_type)

    # we pick the last word as representing our KL type
    kl_type = sub_type.strip().split(' ')[-1]

    # Could this be used to return a value?  If so, mark it as IO
    prefix = ''
    if apply_io and not 'const' in cpp_arg_type:
      if '*' in cpp_arg_type or '&' in cpp_arg_type:
        prefix = 'io '
    # Finally, remove any remaining * characters
    kl_type = prefix + kl_type.replace('*', '')


    # now process any array args
    if args_str:
      # So far, I've only encountered argsstr as array variables
      if args_str[0] == '[':
        # a char array maps to a string
        if kl_type == 'char':
          kl_type = 'String'
        else:
          kl_type = kl_type + args_str # KL supports the same array decl
    return kl_type

def process_function(functionNode):
    if (functionNode.attrib['prot'] != 'public'):
        return ''

    if skipInlineFunctions and functionNode.attrib['inline'] == 'yes':
        return ''

    type_node = functionNode.find('type')
    if type_node == None or 'DEPRECATED' in ET.tostring(type_node, encoding="us-ascii", method="text"):
        return ''

    fnReturns = get_str(type_node)
    fnName = functionNode.find('name').text
    fnArgs = functionNode.findall('param')

    if (fnName in elementsToIgnore):
        return ''

    # Get KL type for return arg
    fnReturns = cpp_to_kl_type(fnReturns)

    klLine = ""
    if (len(fnReturns) > 0):
        klLine = 'function ' + fnReturns + ' ' + fnName + '(';
    else:
        klLine = 'function ' + fnName + '(';

    for i in range(len(fnArgs)):
        arg = fnArgs[i]
        arType = get_str(arg.find('type'))
        arName = get_str(arg.find('declname'))
        arArgsStr = get_str(arg.find('argsstring'))
        # if hte name is not defined, the argument is ignored
        if not arName:
            continue;

        # get the KL type

        arType = cpp_to_kl_type(arType, True, arArgsStr)

        # if we had a C++ default val, indicate what it was
        # Perhaps we could generate 2 functions in this case, one which calls the other.
        ar_def_val = arg.find('defval')
        if (ar_def_val != None):
          arName += "/*=" + get_str(ar_def_val) + "*/"

        if (i > 0):
            klLine += ', '
        klLine += arType + ' ' + arName
    klLine += ') = \'_fe_' + fnName + '\';\n'

    print(klLine)
    return klLine


def _process_struct(struct_node):
    klLine = '';
    # first, find docs
    desc_node = struct_node.find('detaileddescription')
    if (desc_node != None):
        klLine = '/** {0}*/\n'.format(get_str(desc_node))

    # should this element be ignored?
    name = struct_node.find('compoundname').text
    if (name in elementsToIgnore):
      return ''

    klLine += "struct " + name + " {\n"
    for member in struct_node.iter('memberdef'):
        if member.get('kind') == 'variable':
            stType = get_str(member.find('type'))
            stName = member.find('name').text
            stArgsStr = get_str(member.find('argsstring'))
            comment = get_str(member.find('detaileddescription'))
            stType = cpp_to_kl_type(stType, False, stArgsStr)

            # We cannot have a non-typed member, skip it if necessary
            if not stType:
                continue

            klLine += '  ' + stType + ' ' + stName + ';'
            if (comment):
                klLine += ' // ' + comment
            klLine += '\n'

    klLine += '};\n'
    print(klLine)
    return klLine + '\n'


def process_class_or_struct(struct_or_class_node):
    # if this is a reference, dereference it:
    # name = structNode.find('name').text
    # refId = structNode.find('ref')
    ref_id = struct_or_class_node.attrib['refid']
    if (ref_id != None):
        local_file = xmlRootDir + ref_id + '.xml'
        local_doc = ET.parse(local_file)

        compounds = local_doc.findall('compounddef')
        for compound in compounds:
            if (compound.attrib['id'] == ref_id):
                if (compound.attrib['kind'] == 'struct'):
                    return _process_struct(compound)
    return ''


# Handle processing an XML file and writing out the
def process_file(override_name, infilename, outputfile):
    tree = ET.parse(infilename)
    root = tree.getroot()

    file_contents = []

    for class_element in root.iter('innerclass'):
        file_contents.append(process_class_or_struct(class_element))

    # Should we process the sections first of
    for section_def in root.iter('sectiondef'):
        # for each section, get relevant docs
        docs = get_str(section_def.find('header')) + '\n'
        docs += get_str(section_def.find('description'))
        section_contents = []
        #file_contents.append('/**\n' + docs + '\n*/\n\n')

        for processElement in section_def.iter('memberdef'):
            if processElement.attrib['kind'] == 'define':
                res = process_define(processElement)
                if res and len(res) > 0:
                    section_contents.append(res)
            elif processElement.attrib['kind'] == 'function':
                res = process_function(processElement)
                if res and len(res) > 0:
                    section_contents.append(res)

        if len(section_contents) > 0:
            # do we have any actual docs?
            if len(docs) > 2:
                file_contents.append('/**\n' + docs + '\n*/\n\n')
            file_contents += section_contents



    if (len(file_contents) == 0):
        return

    # Write contents out
    f = open(outputfile, 'w')
    # add in the initial documentation
    detaileddesc = get_str(root[0].find('detaileddescription'))
    if detaileddesc:
        f.write('/**\n   ' + detaileddesc + ' \n*/\n\n')

    # Add in 'requires
    for extn in extns_required:
        f.write('require %s;\n' % extn)

    f.write('\n')

    # add in custom overrides
    if override_name in custom_add_to_file:
        f.write(custom_add_to_file[override_name])

    # add in auto-translated KL contents
    f.writelines(file_contents)

#
# Generate an FPM file that KL2EDK can use to generate the
# CPP bindings to call back into our wrapped SDK's library
#
def generate_fpm(processed_files):
    f = open(outputRootDir + project_name + '.fpm.json', 'w')
    f.write(
        '{\n'
        '  "libs": [\n'
        '    "' + project_name + '"\n'
        '  ],\n'
        '  "code" : [\n'
    )
    for pf in processed_files:
        f.write('    "' + pf + '",\n')
    f.write('  ]\n')
    f.write('}')

# first, load in the index, get the file list.

tree = ET.parse(xmlRootDir + 'index.xml')
root = tree.getroot()

# Build a list of all parsed files
allFiles = []
for doxyElement in root.iter('compound'):
    if (doxyElement.attrib['kind'] == 'file'):
        fileTuple = [doxyElement.find('name').text, doxyElement.attrib['refid']]
        allFiles.append(fileTuple)

processed_files = []
for aFile in filesToProcess:
    # find the xml file for this header
    processed = False
    for xmlFileLink in allFiles:
        if xmlFileLink[0] == aFile:
            print('Processing: ' + aFile)
            out_file_name = aFile.split('.')[0] + '.kl'
            processed_files.append(out_file_name)
            process_file(aFile, xmlRootDir + xmlFileLink[1] + '.xml', outputRootDir + out_file_name)
            processed = True
            break

    if not processed:
        raise ValueError("File: '%s' not found in doxygen generated files'" % aFile)

# Our last step, generate the FPM file from the converted files.
generate_fpm(processed_files)
