from __future__ import nested_scopes
import shutil
import xml.etree.ElementTree as ET
import re
import sys
import json
import jsonmerge
import os

# we will auto-generate our JSON codegen file as well, as we
# already have most of the data for what is required.

# This dictionary contains all the auto-generated type-mapping
# after execution, this should contain a list of dictionaries
# with the type-conversion info in it.
json_codegen_typemapping = {}
# This dictionary contains the auto-generated function
# implementations.
json_codegen_functionbodies = {}

# keep a list of all functions that contain aliased params
# in MassageCPP we will process the aliases to ensure they
# are converted to the correct C++ types
functions_with_aliases = {}

#
# TODO
#
cpp_typedefs = {}

# we hold a list of all class definitions
# that we can automatically cast to/from
autogen_class_typemapping = []

# Get KL version so we can support newer features
def get_kl_version():
    from subprocess import Popen, PIPE

    p = Popen(['kl', '--version'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    version = output.split()[-1]
    return version.split('.')
kl_version = get_kl_version()


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

#
# parse out the MS Sal declaration
#
def parse_ms_sal(cpp_arg_type):
    prefix = ''
    postfix = ''
    components = cpp_arg_type.split()

    # FE2.0 added support for 'out' as a keyword
    out_spec = 'io '
    if int(kl_version[0]) >= 2:
        out_spec = 'out '

    if len(components) > 1:

        sal_decl = cpp_arg_type.split()[0]
        # Remove the _COM prefix, if it exists
        if sal_decl.startswith('_COM_'):
            sal_decl = sal_decl[4:]

        if sal_decl.startswith('_In_'):
            prefix = 'in '
        if sal_decl.startswith('_Out_'):
            prefix = out_spec
        if sal_decl.startswith('_Inout_'):
            prefix = 'io '
        if sal_decl.startswith('_Outptr_'):
            prefix = out_spec

        # If we have a SAL declaration, does it specify
        # an in/out array?
        if prefix:
            sal_decl = cpp_arg_type.split()[0]
            if '_Opt_' in sal_decl:
                prefix += '/*opt*/'
            if not postfix:
                if '_writes_' in sal_decl or '_reads_' in sal_decl or '_updates_' in sal_decl:
                    postfix = '[]'
    return (prefix,postfix)

#
# Make our best-guess if an argument is in/out.  Basically,
# we assume that any non-const pointer is IO
#
def guess_sal(cpp_arg_type):
    if not 'const' in cpp_arg_type:
      if '*' in cpp_arg_type or '&' in cpp_arg_type:
        return 'io '
    return ''

#
# Create a regular expression  from the dictionary keys
#
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
    postfix = ''
    if use_ms_sal:
        prefix,postfix = parse_ms_sal(cpp_arg_type)
    if (not prefix) and apply_io:
        prefix = guess_sal(cpp_arg_type)

    # Finally, remove any remaining * characters
    kl_type = kl_type.replace('*', '')

    # We can (very) safely assume that only one of
    # postfix or args_str is not-null.
    if args_str:
        postfix = args_str
    # now process any array args
    if postfix:
      # So far, I've only encountered argsstr as array variables (eg, int var[10];)
      if postfix[0] == '[':
        if kl_type == 'char':
            kl_type = 'String'
        if kl_type == 'String':
          # we assume if we have a char pointer, its always just a string
          postfix = ''

    return prefix + kl_type + postfix


# split_name_type = re.compile(r'\s*(.*?)\s*([\w]+)\s*$')
# def process_fn_pointer(fn_ptr_node):
#     # First, lets detect if this is a function pointer 
#     # or not (Doxygen does not tell us this one)
#     # We will assume that all function pointers look like:
#     # retVal(*fn_name)(args...)
#     # To detech a function pointer, we will search for the double brackets
#     # This will need a lot of revision likely as we work
#     # on new APIs with differing conventions
#     args_node = fn_ptr_node.find('argsstring')
#     if def == None:
#         return False
#     args_str = args_node.text
#     if args_str[:2] != ')(':
#         return False
#     args_str = args_str[2:-1]

#     # we have a function pointer - lets get to work!
#     # First - is this element already ignored?
#     fn_name = fn_ptr_node.find('name').text
#     if (fn_name in elementsToIgnore):
#         return False

#     type_node = fn_ptr_node.find('type')
#     if type_node == None or 'DEPRECATED' in ET.tostring(type_node, encoding="us-ascii", method="text"):
#         return False

#     cpp_returns = get_str(type_node)
#     bidx = cpp_returns.find('(')
#     if not bidx:
#         return False

#     cpp_returns = cpp_returns[:bidx]

#     # While building the line to write into the KL file
#     # we also build the line we'll add to the autogen file
#     # Essentially, but the end of this function the auto-gen
#     # line should call the native function we are processing
#     # with the converted types that will be generated by
#     # kl2edk utility
#     autogen_line = fn_name + '('

#     # Get KL type for return arg
#     kl_returns = cpp_to_kl_type(cpp_returns)

#     klLine = ""
#     if kl_returns:
#         klLine = kl_returns + ' ' + fn_name + '(';
#     else:
#         klLine = fn_name + '(';

#     fe_fn_tag = '_fe_'
#     fe_fn_name = fe_fn_tag + fn_name

#     all_args = args_str.split(',')
#     for i in range(len(all_args)):
#         arg = all_args[i]
#         # For each argument, try to find the name and type
#         type_name = split_name_type.match(arg)
#         cpp_type = ''
#         cpp_name = '_val' + str(i)
#         if type_name[0]:
#             cpp_type = type_name[0]
#             cpp_name = type_name[1]
#         else:
#             cpp_type = type_name[1]

#         # get the KL type
#         kl_type = cpp_to_kl_type(cpp_type, True)


#         # if our KL type is alias'ed, then save the name
#         # of this function.  This is because we will need
#         # to fix up the conversion functions in MassageCPP
#         if kl_type in kl_type_aliases:
#             if fe_fn_name not in functions_with_aliases:
#                 functions_with_aliases[fe_fn_name] = []
#             functions_with_aliases[fe_fn_name].append([kl_type, arName])

#         if (i > 0):
#             klLine += ', '
#             autogen_line += ', '

#         klLine += kl_type + ' ' + arName

#         # If there are more '*' in the CPP type than we expect
#         # (based on the ctype in our codegen) then we will need
#         # to pass this parameter by address.
#         base_kl_type = kl_type.rsplit(None, 1)[-1]
#         if base_kl_type in json_codegen_typemapping:
#             if cpp_type.count('*') > json_codegen_typemapping[base_kl_type]['ctype'].count('*'):
#                 autogen_line += '&'

#         # finally, add the name to the autogen line.
#         autogen_line += parameter_prefix + arName.capitalize()

#     klLine += ')'
#     autogen_line += ')'

#     # If we return, we need to create the return value parameter
#     if kl_returns:
#         to_fn = json_codegen_typemapping[kl_returns]['to']
#         res = '%s_result' % parameter_prefix
#         if kl_returns in kl_pod_types:
#             autogen_line = '  %s %s = %s;\n  Fabric::EDK::KL::%s _result;\n  %s(%s, _result);\n' % (cpp_returns, res, autogen_line, kl_returns, to_fn, res)
#         else:
#             autogen_line = '  %s %s = %s;\n  %s(%s, _result);' % (cpp_returns, res, autogen_line, to_fn, res)
#     else:
#         autogen_line = '  %s;\n' % autogen_line

#     # We remember our auto-genned lined for later reference
#     json_codegen_functionbodies[fe_fn_name] = autogen_line

#     # Now - where we really diverge from the simple function extraction, for a 
#     # function pointer we cannot just generate a function pointer - we need to 
#     # generate a full interface to define that defines the function
#     klLine = "interface %s { \n  %s;\n};\n" % (fn_name, klLine)

#     print(klLine)
#     return klLine

#
# We collect all typedef's, so when we are processing KL
# we can know if any class we are processing has been typedeffed
# Doxygen sorts elements into different sections, but we want/need to put
# any typedef's after the class/enum being typedef'ed
# We do this by pre-processing all typedef's and then
# when each class/struct/enum is actually declared
# we add the typedef (or alias in KL-speak) immediately after
def preprocess_typedef(typedef_node):
    name = typedef_node.find('name').text
    if (name in elementsToIgnore):
        return

    # if this name already has an explicit mapping leave it alone
    if name in cppToKLTypeMapping:
        return

    # the alias type is the name, but we drop qualifieres
    type = get_str(typedef_node.find('type'))
    type = type.split()[-1]

    # Skip redundant C-style definitions like:
    # typedef interface IKinectSensor IKinectSensor
    if type == name:
        return

    # If this is a function-pointer typedef,
    # we will figure out exactly how to handle
    # this much much later...
    if '(' in type:
        return

    cpp_typedefs[type] = name

#
# if the named item is in our lists of alias's, append
# the alias definition to the str list
#
def maybe_make_alias(type):
    if type in kl_type_aliases:
        return 'alias %s %s;\n' % (type, kl_type_aliases.pop(type))
    if type in cpp_typedefs:
        return 'alias %s %s;\n' % (type, cpp_typedefs.pop(type))
    return ''

def process_enum(enum_node):
    name = enum_node.find('name').text
    if (name in elementsToIgnore):
        return ''

    str = []
    str.append('// Enum values for : %s ' % name)
    # An enum is always aliased in KL
    str.append('alias UInt32 %s;' % name)
    
    values = enum_node.findall('enumvalue')
    last_val = 0
    for v in values:
        value_name = get_str(v.find('name'))
        value_init = get_str(v.find('initializer'))
        value_desc = get_str(v.find('briefdescription'))

        if not value_init or len(value_init) <= 1:
            value_init = last_val
            last_val = last_val + 1
        else:
            # if a value is defined, save it
            # so the next value can/will increment it
            try:
                last_val = int(value_init[1:], 0)
            except ValueError:
                print("Error casting: %s to integer" % value_init)
        
        if value_desc and len(value_desc) > 1:
            value_desc = " // " + value_desc

        str.append("const %s %s %s;%s" % (name, value_name, value_init, value_desc))

    alias = maybe_make_alias(name)
    if alias:
        str.append(alias)

    return "\n".join(str) + '\n\n'

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

def _param_name(name):
    return parameter_prefix + name[:1].capitalize() + name[1:]

def process_function(functionNode, class_name=''):
    if (functionNode.attrib['prot'] != 'public'):
        return ''

    if skipInlineFunctions and functionNode.attrib['inline'] == 'yes':
        return ''

    type_node = functionNode.find('type')
    if type_node == None or 'DEPRECATED' in ET.tostring(type_node, encoding="us-ascii", method="text"):
        return ''

    cpp_returns = get_str(type_node)
    fn_name = functionNode.find('name').text
    fnArgs = functionNode.findall('param')

    if (fn_name in elementsToIgnore):
        return ''

    fe_fn_tag = '_fe_'
    if class_name:
        fe_fn_tag += class_name + "_"
    fe_fn_name = fe_fn_tag + fn_name

    # While building the line to write into the KL file
    # we also build the line we'll add to the autogen file
    # Essentially, but the end of this function the auto-gen
    # line should call the native function we are processing
    # with the converted types that will be generated by
    # kl2edk utility
    autogen_line = fn_name + '('

    # Get KL type for return arg
    kl_returns = cpp_to_kl_type(cpp_returns)

    kl_class_prefix = ' ';
    if len(class_name) > 1:
       kl_class_prefix = ' ' + class_name + "."

    klLine = ""
    if kl_returns:
        klLine = 'function ' + kl_returns + kl_class_prefix + autogen_line;
    else:
        klLine = 'function' + kl_class_prefix + autogen_line;
    
    kl_prefix = ''

    for i in range(len(fnArgs)):
        arg = fnArgs[i]
        cpp_type = get_str(arg.find('type'))
        arName = get_str(arg.find('declname'))
        arArgsStr = get_str(arg.find('argsstring'))

        # skip varargs
        if cpp_type == '...':
            continue

        # if hte name is not defined, we give it a default value
        # (its legal c++ syntax to define void f(char* )
        if not arName:
            arName = '_val'

        # get the KL type
        kl_type = cpp_to_kl_type(cpp_type, True, arArgsStr)
        # some types (eg void) simply don't exist in KL
        if not kl_type:
            continue

        # remove in/out KL semantics
        base_kl_type = kl_type.rsplit(None, 1)[-1]
        
        # if our KL type is alias'ed, then save the name
        # of this function.  This is because we will need
        # to fix up the conversion functions in MassageCPP
        if base_kl_type in kl_type_aliases:
            if fe_fn_name not in functions_with_aliases:
                functions_with_aliases[fe_fn_name] = []
            functions_with_aliases[fe_fn_name].append([base_kl_type, arName])

        # if we had a C++ default val, indicate what it was
        # Perhaps we could generate 2 functions in this case, one which calls the other.
        ar_def_val = arg.find('defval')
        if (ar_def_val != None):
          arName += "/*=" + get_str(ar_def_val) + "*/"

        if (i > 0):
            klLine += ', '
            autogen_line += ', '

        klLine += kl_type + ' ' + arName

        # If there are more '*' in the CPP type than we expect
        # (based on the ctype in our codegen) then we will need
        # to pass this parameter by address.
        
        if base_kl_type in json_codegen_typemapping:
            if cpp_type.count('*') > json_codegen_typemapping[base_kl_type]['ctype'].count('*'):
                autogen_line += '&'

        # finally, add the name to the autogen line.
        autogen_param_name = _param_name(arName)
        autogen_line += autogen_param_name

    klLine += ') = \'' + fe_fn_name + '\';\n'
    autogen_line += ')'

    # If we return, we need to create the return value parameter
    if kl_returns:
        to_fn = ''
        if kl_returns in json_codegen_typemapping:
            to_fn = json_codegen_typemapping[kl_returns]['to']
            
        res = '%s_result' % parameter_prefix
        kl_base_returns = kl_type_aliases.get(kl_returns, kl_returns)
        if kl_base_returns in kl_pod_types:
            autogen_line = '  %s %s = %s;\n  Fabric::EDK::KL::%s _result;\n  %s(%s, _result);\n' % (cpp_returns, res, autogen_line, kl_returns, to_fn, res)
        else:
            autogen_line = '  %s %s = %s;\n  %s(%s, _result);' % (cpp_returns, res, autogen_line, to_fn, res)
    else:
        autogen_line = '  %s;\n' % autogen_line

    # We remember our auto-genned lined for later reference
    json_codegen_functionbodies[fe_fn_name] = kl_prefix + autogen_line

    print(klLine)
    return klLine

# set first letter to lowercase
# used to ensure all class/struct members have lower
# case first letters.  Necessary on KinectSDK
# because of the habit of naming variables
# the same as their type
def first_to_lower(s):
    return s[:1].lower() + s[1:] if s else ''

def _process_class_or_struct(struct_node, kl_type):
    klLine = '';
    # first, find docs
    desc_node = struct_node.find('detaileddescription')
    if (desc_node != None):
        klLine = '/** {0}*/\n'.format(get_str(desc_node))

    # should this element be ignored?
    name = struct_node.find('compoundname').text
    if (name in elementsToIgnore):
      return ''

    # Has this class been alias'ed to a KL type?  If so, we only
    # want to output the alias, not the whole type
    alias_type = name
    while alias_type in cpp_typedefs:
        alias_type = cpp_typedefs[alias_type]
    if alias_type in kl_type_aliases:
        return 'alias %s %s;\n' % (kl_type_aliases[alias_type], alias_type)

    # begin defining our KL class.

    klLine += kl_type + " " + name + " {\n"
    # Now, test to see if this class/struct has any functions
    # attached to it.  If it does (and there is no defined
    # conversion function) we assume we will need to maintain
    # a pointer to the native handle, and refer to this when
    # calling functions
    has_functions = False and kl_type != 'struct'
    for function in struct_node.iter('memberdef'):
        if function.get('kind') == 'function':
            has_functions = True

            # Generate conversions for our classes.  This will
            # be virtually identical to the opaque wrappers
            conversion = _get_typemapping(name, name, True)
            json_codegen_typemapping[name] = conversion
            autogen_class_typemapping.append(name)
            break

    if has_functions:
        klLine += "\tData _handle;\n"

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

            # C++ seems to allow naming variables the same as their types. we do not.
            stName = first_to_lower(stName)
            if stType == stName:
                stName = '_%s' % stName

            klLine += '  ' + stType + ' ' + stName + ';'
            if comment and (len(comment) > 1):
                klLine += ' // ' + comment
            klLine += '\n'

    klLine += '};\n\n'

    klLine += maybe_make_alias(name)

    # once the struct is defined, add any/all functions to it.
    has_functions = False
    for function in struct_node.iter('memberdef'):
        if function.get('kind') == 'function':
            has_functions = True
            klLine += process_function(function, name)

    print(klLine)
    return klLine + '//////////////////////////////////////////\n'

def process_class_or_struct(struct_or_class_node):
    # if this is a reference, dereference it:
    # name = structNode.find('name').text
    # refId = structNode.find('ref')
    ref_id = struct_or_class_node.attrib['refid']
    if (ref_id != None):
        local_file = os.path.join(xml_path, ref_id + '.xml')
        local_doc = ET.parse(local_file)

        compounds = local_doc.findall('compounddef')
        for compound in compounds:
            if (compound.attrib['id'] == ref_id):
                if (compound.attrib['kind'] == 'struct'):
                    return _process_class_or_struct(compound, 'struct')
                if (compound.attrib['kind'] == 'class'):
                    return _process_class_or_struct(compound, 'object')
    return ''


# Handle processing an XML file and writing out the
def process_file(override_name, infilename, outputfile):
    tree = ET.parse(infilename)
    root = tree.getroot()

    file_contents = []

    # First, collect all the typedef's
    for section_def in root.iter('sectiondef'):
        for processElement in section_def.iter('memberdef'):
            if processElement.attrib['kind'] == 'typedef':
                preprocess_typedef(processElement)

    # Our first pass through emits all the info we know
    # doesn't depend on other things (enum's only?)
    file_contents += ["//////////////////////////////////////////////////\n//  enumerated values\n"]
    for section_def in root.iter('sectiondef'):
        section_contents = ['\n']
        for processElement in section_def.iter('memberdef'):
            if processElement.attrib['kind'] == 'enum':
                res = process_enum(processElement)
                if res and len(res) > 0:
                    section_contents.append(res)
            elif processElement.attrib['kind'] == 'define':
                res = process_define(processElement)
                if res and len(res) > 0:
                    section_contents.append(res)

        if len(section_contents) > 1:
            file_contents += section_contents

    # Always have class declarations at the top of the file
    file_contents += ["//////////////////////////////////////////////////\n//  classes \n"]
    for class_element in root.iter('innerclass'):
        file_contents.append(process_class_or_struct(class_element))

    # add in custom overrides after class declarations
    if override_name in custom_add_to_file:
        file_contents.append(custom_add_to_file[override_name] + '\n\n')


    # Last we add in any file-scoped functions.  These are most likely to
    # depend on the previous definitions.
    file_contents += ["//////////////////////////////////////////////////\n//  global-scope functions \n"]
    for section_def in root.iter('sectiondef'):
        # for each section, get relevant docs
        docs = get_str(section_def.find('header')) + '\n'
        docs += get_str(section_def.find('description'))
        section_contents = ['\n']
        #file_contents.append('/**\n' + docs + '\n*/\n\n')

        for processElement in section_def.iter('memberdef'):
            #if processElement.attrib['kind'] == 'define':
            #    res = process_define(processElement)
            #    if res and len(res) > 0:
            #        section_contents.append(res)
            #elif processElement.attrib['kind'] == 'enum':
            #    res = process_enum(processElement)
            #    if res and len(res) > 0:
            #        section_contents.append(res)
            if processElement.attrib['kind'] == 'function':
                res = process_function(processElement)
                if res and len(res) > 0:
                    section_contents.append(res)
            #elif processElement.attrib['kind'] == 'typedef':
            #    res = process_typedef(processElement)
            #    if res and len(res) > 0:
            #        section_contents.append(res)

        if len(section_contents) > 1:
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

    # add in auto-translated KL contents
    f.writelines(file_contents)

##################################################################################
# Code-genning files

def _generate_typemapping_header(full_json, filename, skip_kl_type, fn_body):
    fh = open(os.path.join(output_h_dir, filename), 'w')

    fh.write(
    '/* \n'
    ' * This auto-generated file contains typemapping conversion fn\n'
    ' * declarations for the data types found in %s codegen file\n'
    ' *  - Do not modify this file, it will be overwritten\n'
    ' */\n\n\n#pragma once\n' % (project_name)
    )

    typemapping = full_json['typemapping']
    for key, val in typemapping.iteritems():
        kl_type = key

        # Skip opaque types - they will be generated
        # separately (we know the full implementation for
        # those functions)
        if kl_type in opaque_type_wrappers:
            continue

        if skip_kl_type(kl_type):
            continue

        if kl_type[-2:] == '[]':
            kl_type = 'VariableArray< Fabric::EDK::KL::%s >' % kl_type[:-2]

        cpp_type = val['ctype']
        sfrom = val['from']
        sto = val['to']
        
        from_fn = ( 'inline bool %s(const Fabric::EDK::KL::%s & from, %s & to) { \n'
                    '  %s\n'
                    '  return true;\n'
                    '}\n\n' % (sfrom, kl_type, cpp_type, fn_body))

        fh.write(from_fn)

        # When passing pointer values by-reference, we need
        # to const the reference in order for the cast to const
        # to succeed.
        # https://stackoverflow.com/questions/2908244/why-no-implicit-conversion-from-pointer-to-reference-to-const-pointer
        _fn_body = '' + fn_body
        if '*' in cpp_type:
            # If we try to do a pointer assignment, then the const-ness 
            # trips us up.  De-const all input pointers on assignment
            _fn_body = _fn_body.replace('from', 'const_cast<%s>(from)' % cpp_type)
            cpp_type = cpp_type + ' const'

        to_fn = ('inline bool %s(const %s & from, Fabric::EDK::KL::%s & to) {\n'
                '  %s\n'
                '  return true; \n'
                '}\n\n' % (sto, cpp_type, kl_type, _fn_body))
        fh.write(to_fn)

def skip_nonpod(kl_type):
    # for all POD conversions we can simply do an equals
    kl_base_type = kl_type_aliases.get(kl_type, kl_type)
    if kl_base_type in kl_pod_types:
        return False
    return True;

def generate_typemapping_header(full_json):
    _generate_typemapping_header(full_json, '_pod_typemapping.h', skip_nonpod, 'to = from;')
    _generate_typemapping_header(full_json, '_typemapping.h', lambda x: not skip_nonpod(x), '#pragma message("Implement Me")')


# For each opaque struct, we can auto-generate the C++ code
# to convert to/from the KL type
def generate_opaque_cpp_conv():
    fh = open(os.path.join(output_h_dir, opaque_file_name + '.h'), 'w')
    fh.write(
    '/* \n'
    ' * This auto-generated file contains simple conversion fn\n'
    ' * declarations for the opaque data-types found in %s\n'
    ' *  - Do not modify this file, it will be overwritten\n'
    ' */\n'
    '\n'
    '#pragma once\n\n' % (project_name)
    )

    for opaque_type in opaque_type_wrappers:
        sfrom = 'KL' + opaque_type + '_to_CP' + opaque_type
        sto = 'CP' + opaque_type + '_to_KL' + opaque_type
        fh.write(
            '#include "%s.h"\n'
            'inline bool %s(const Fabric::EDK::KL::%s & from, %s* & to) {\n'
            '  to = reinterpret_cast<%s>(from._handle); \n'
            '  return true; \n'
            '}\n\n' % (opaque_type, sfrom, opaque_type, opaque_type, opaque_type + '*')
        )

        fh.write(
            'inline bool %s(const %s* const& from, Fabric::EDK::KL::%s & to) {\n'
            '  to._handle = const_cast<%s*>(from); \n'
            '  return true; \n'
            '}\n\n' % (sto, opaque_type, opaque_type, opaque_type)
            )

    for class_type in autogen_class_typemapping:
        sfrom = 'KL' + class_type + '_to_CP' + class_type
        sto = 'CP' + class_type + '_to_KL' + class_type
        fh.write(
            '#include "%s.h"\n'
            'inline bool %s(const Fabric::EDK::KL::%s & from, %s* & to) {\n'
            '  to = reinterpret_cast<%s>(from->_handle); \n'
            '  return true; \n'
            '}\n\n' % (class_type, sfrom, class_type, class_type, class_type + '*')
        )

        fh.write(
            'inline bool %s(const %s* const& from, Fabric::EDK::KL::%s & to) {\n'
            '  to->_handle = const_cast<%s*>(from); \n'
            '  return true; \n'
            '}\n\n' % (sto, class_type, class_type, class_type)
            )
        

#
# We want to write out a file containing all aliases
# These aliases can be manually set or be generated
# from typedef's and enums
#
#def generate_alias_file():
#    filename = kl_alias_file_name + '.kl'
#    f = open(os.path.join(output_dir, filename), 'w')
#    f.write(
#        '/* \n'
#        ' * This auto-generated file contains aliases for all\n'
#        ' * type renamings in ' + project_name + '\n'
#        ' *  - Do not modify this file, it is auto-generated\n'
#        ' */\n\n'
#    )

    # we add in the aliases here (for lack of a better place)
#    f.write('// Aliases help us differentiate the correct\n//return type when converting KL to C++ types later\n')
#    for alias, kl_type in kl_type_aliases.iteritems():
#        f.write(
#            'alias %s %s;\n' % (kl_type, alias)
#        )
#    return filename
#
# Write out simple wrapper structs for opaque data types.
# These structs are collected in a file that is written out
# as the first file in a project (so that following files
# can refer to it's definitions
#
def generate_opaque_file():
    f = open(os.path.join(output_dir, opaque_file_name + '.kl'), 'w')
    f.write(
        '/* \n'
        ' * This auto-generated file contains simple wrapper\n'
        ' * structs for the opaque data-types found in ' + project_name + '\n'
        ' *  - Do not modify this file, it will be overwritten\n'
        ' */\n\n'
    )
    # Add in 'requires
    for extn in extns_required:
        f.write('require %s;\n' % extn)

    # we add in the aliases here (for lack of a better place)
    f.write('// Aliases help us differentiate the correct\n//return type when converting KL to C++ types later\n')
    for alias, type in kl_type_aliases.iteritems():
        kl_type = cpp_to_kl_type(type)
        f.write(
            'alias %s %s;\n' % (kl_type, alias)
        )
    for type, alias in cpp_typedefs.iteritems():
        # We skip the alias if it has been output already
        if alias in kl_type_aliases:
            continue
        kl_type = cpp_to_kl_type(type)
        f.write(
            'alias %s %s;\n' % (kl_type, alias)
        )

    for opaque_type in opaque_type_wrappers:
        f.write(
            '\n'
            'struct ' + opaque_type + ' {\n'
            '  Data _handle;\n'
            '};\n'
            'Boolean ' + opaque_type + '.isValid() { return this._handle != Data(); }\n'
        )

    generate_opaque_cpp_conv()

#
# Generate an FPM file that KL2EDK can use to generate the
# CPP bindings to call back into our wrapped SDK's library
#
def generate_fpm(processed_files):
    f = open(os.path.join(output_dir, project_name + '.fpm.json'), 'w')
    f.write(
        '{\n'
        '  "libs": [\n'
        '    "' + project_name + '"\n'
        '  ],\n'
        '  "code" : [\n'
    )
    for pf in processed_files:
        f.write('    "' + pf + '",\n')

    # For any custom KL files,
    # add them to the FPM list
    if custom_KL_dir:
        custom_files = glob.glob(custom_KL_dir + '/*.kl')
        for file in custom_files:
            f.write('    "' + os.path.basename(file) + '",\n')

    f.write('  ]\n')
    f.write('}')

#
# Build a code-gen compatible type mapping from our typemapping
#
def _get_typemapping(c_type, kl_type, is_pointer):
    conversion = ( {
            'ctype': c_type,
            'from' : 'KL%s_to_CP%s' % (kl_type, c_type),
            'to' : 'CP%s_to_KL%s' % (c_type, kl_type),
        })
    if is_pointer:
        conversion['ctype'] = c_type + '*'
        conversion['methodop'] = '->'
    else:
        conversion['methodop'] = '.'
    return conversion

def get_auto_codegen_typemapping():
    typemapping = {}

    # generate conversions for our CPP To KL types
    for cpp_type, kl_type in cppToKLTypeMapping.iteritems():
        # Do not translate types that KL has removed (eg - void)
        if not kl_type:
            continue

        cpp_raw_type = cpp_type.replace('*', '')
        cpp_raw_type = cpp_raw_type.replace(' ', '_')
        kl_raw_type = kl_type.replace('[]', 'Arr')
        conversion = ( {
            'ctype': cpp_type,
            'from' : kl_raw_type + '_to_' + cpp_raw_type,
            'to' : cpp_raw_type + '_to_' + kl_raw_type,

        })
        if '*' in cpp_type:
            conversion['methodop'] = '->'
        else:
            conversion['methodop'] = '.'

        conversion = _get_typemapping(cpp_raw_type, kl_raw_type, '*' in cpp_type)

        typemapping[kl_type] = conversion

    # generate conversions for alias'ed types
    # (We assume that an alias'ed type reflects
    # a C++ class)
    for alias_type, base_type in kl_type_aliases.iteritems():
        # We cannot know if the type should be pointer-based,
        # but we can assume that most of the time it won't be
        conversion = _get_typemapping(alias_type, base_type, False)
        typemapping[alias_type] = conversion

    # Generate conversions for our opaque wrappers
    #  This will be pretty simple - just wrapping the
    # returned pointer with a KL data member
    for opaque_type in opaque_type_wrappers:
        conversion = _get_typemapping(opaque_type, opaque_type, True)
        typemapping[opaque_type] = conversion

    return typemapping

#
# Generate a <ProjectName>.codegen.json file to complement our FPM
# This will transfer any type-specific info we know here into the
# auto-generated C++ code our KL files call into
#
def generate_auto_codegen():

    #type_mapping = get_auto_codegen_typemapping()
    # create the full Codegen JSON repr
    full_json = {}
    full_json['parameterprefix'] = parameter_prefix
    full_json['typemapping'] = json_codegen_typemapping
    full_json['functionbodies'] = json_codegen_functionbodies

    # We don't have any parameterconversionstoskip or methodmapping - do we need 'em?

    json_filename = os.path.join(output_dir, project_name + '.auto.codegen.json')
    with open(json_filename, 'w') as outfile:
        json.dump(full_json, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

    return full_json

#
# We allow users to add an 'override' codegen file that we
# merge with out own file.
#
def generate_codegen():
    auto_codegen = generate_auto_codegen()

    # merge file is the users manually specified file
    final_file = os.path.join(output_dir, project_name + '.codegen.json')

    merge_file_path = os.path.join(root_dir, merge_codegen_file)
    if os.path.isfile(merge_file_path):

        with open(merge_file_path) as json_file:
            merge_codegen = json.load(json_file)
            final_codegen = jsonmerge.merge(auto_codegen, merge_codegen)

            # generate a header file for conversion functions
            generate_typemapping_header(final_codegen)

            # write out the result
            with open(final_file, 'w') as outfile:
                json.dump(final_codegen, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
    else:
        # with nothing to merge, write out the auto-file as the full codegen file
        with open(final_file, 'w') as outfile:
            json.dump(auto_codegen, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

####################################################################################################
#
# Begin:
# first, load in the index, get the file list.
#
xml_path = os.path.join(root_dir, xml_dir)
tree = ET.parse(os.path.join(xml_path, 'index.xml'))
root = tree.getroot()

# Build a list of all parsed files
allFiles = []
for doxyElement in root.iter('compound'):
    if (doxyElement.attrib['kind'] == 'file'):
        fileTuple = [doxyElement.find('name').text, doxyElement.attrib['refid']]
        allFiles.append(fileTuple)

processed_files = []

# Build conversion fn's
json_codegen_typemapping = get_auto_codegen_typemapping();
# We need the full conversion fn list (even manually spec ones)
# This is because when auto-genning fn's we need the conv fns
# for building the return values
merge_file_path = os.path.join(root_dir, merge_codegen_file)
with open(merge_file_path) as json_file:
    merge_codegen = json.load(json_file)
    json_codegen_typemapping = jsonmerge.merge(json_codegen_typemapping, merge_codegen['typemapping'])

for aFile in filesToProcess:
    # find the xml file for this header
    processed = False
    for xmlFileLink in allFiles:
        if xmlFileLink[0] == aFile:
            print('Processing: ' + aFile)
            out_file_name = aFile.split('.')[0] + '.kl'
            processed_files.append(out_file_name)
            process_file(aFile, os.path.join(xml_path, xmlFileLink[1] + '.xml'), os.path.join(output_dir, out_file_name))
            processed = True
            break

    if not processed:
        raise ValueError("File: '%s' not found in doxygen generated files'" % aFile)

# last, generate our opaque datatypes
if opaque_type_wrappers or kl_type_aliases:
    generate_opaque_file()
    processed_files = [opaque_file_name + '.kl'] + processed_files

#if kl_type_aliases:
#    alias_filename = generate_alias_file()
#    processed_files = [alias_filename] + processed_files

# Our last step, generate the FPM file from the converted files.
generate_fpm(processed_files)
generate_codegen()
