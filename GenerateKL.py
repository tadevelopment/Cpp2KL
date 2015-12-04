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

############################################################
#
# parse out the MS Sal declaration
#
def _parse_sal_postfix(sal_decl, components, kl_type):
    # is this a pointer based type?
    num_ptrs = components[-1].count('*')
    postfix = ''
    if kl_type != 'String' or num_ptrs > 1:
        fn_postfix = ''
        if '_writes_' in sal_decl or '_reads_' in sal_decl or '_updates_' in sal_decl:
            postfix = '[]'
            fn_postfix = 'Ar'
        elif sal_decl.startswith('_Outptr_result_buffer_'):
            postfix = '<>'
            fn_postfix = 'ExAr'
                
        if postfix:
            # Auto-gen conversion fn's
            full_kl_type = kl_type + postfix
            if full_kl_type not in json_codegen_typemapping:
                cpp_type = components[-1]
                cpp_type = cpp_type.replace('*', '')
                conversion = _get_typemapping(cpp_type, kl_type + fn_postfix, num_ptrs)
                json_codegen_typemapping[full_kl_type] = conversion
    return postfix


def parse_ms_sal(cpp_arg_type, kl_type):
    prefix = ''
    postfix = ''
    components = cpp_arg_type.replace(' *', '*').split()

    # FE2.0 added support for 'out' as a keyword
    out_spec = 'io '
    #if int(kl_version[0]) >= 2:
    #    out_spec = 'out '

    if len(components) > 1:

        sal_decl = components[0]
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
            if '_Opt_' in sal_decl:
                prefix += '/*opt*/'

            if not postfix:
                postfix = _parse_sal_postfix(sal_decl, components, kl_type)

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
    cpp_base_type = sub_type.strip().split(' ')[-1]

    # special case - for all string representations we want to use String
    base_kl_type = kl_type_aliases.get(cpp_base_type, kl_type)
    if base_kl_type == 'String':
        kl_type = base_kl_type
    else:
        # Finally, remove any remaining * characters
        kl_type = cpp_base_type.replace('*', '')
        

    # Could this be used to return a value?  If so, mark it as IO
    prefix = ''
    postfix = ''
    if use_ms_sal:
        prefix,postfix = parse_ms_sal(cpp_arg_type, kl_type)
    if (not prefix) and apply_io:
        prefix = guess_sal(cpp_arg_type)

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
        if kl_type_aliases.get(cpp_base_type, kl_type) == 'String':
            # we assume if we have a char pointer, its always just a string
            postfix = ''
            kl_type = 'String'
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

# We store a list of all enums, because in the kl2edk code
# the enums are converted to/from UINTs, and we need
# to explicitly cast between.  We test params against
# the enum types, and if it is an enum, do the cast
all_enums = []
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

    all_enums.append(cpp_typedefs.get(name, name))
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
    if class_name:
        autogen_line = _param_name('this_') + '->' + autogen_line

    # Get KL type for return arg
    kl_returns = cpp_to_kl_type(cpp_returns)

    kl_class_prefix = ' ';
    if len(class_name) > 1:
       kl_class_prefix = ' ' + class_name + "."

    klLine = ""
    if kl_returns:
        klLine = 'function ' + kl_returns + kl_class_prefix + fn_name + '(';
    else:
        klLine = 'function' + kl_class_prefix + fn_name + '(';
    
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
        for key, val in kl_type_aliases.iteritems():
            if key in cpp_type:
                if fe_fn_name not in functions_with_aliases:
                    functions_with_aliases[fe_fn_name] = []
                functions_with_aliases[fe_fn_name].append([key, arName])

        # if we had a C++ default val, indicate what it was
        # Perhaps we could generate 2 functions in this case, one which calls the other.
        ar_def_val = arg.find('defval')
        if (ar_def_val != None):
          arName += "/*=" + get_str(ar_def_val) + "*/"

        if (i > 0):
            klLine += ', '
            autogen_line += ', '

        klLine += kl_type + ' ' + arName

        # finally, add the name to the autogen line.
        autogen_param_name = _param_name(arName)

        # If there are more '*' in the CPP type than we expect
        # (based on the ctype in our codegen) then we will need
        # to pass this parameter by address.
        
        if base_kl_type in json_codegen_typemapping:
            if cpp_type.count('*') > json_codegen_typemapping[base_kl_type]['ctype'].count('*'):
                autogen_param_name = '&' + autogen_param_name
        else:
            if cpp_type.count('*') > 0:
                autogen_param_name = '&' + autogen_param_name

        # Damn enum's won't cast automatically in C++, and KL2EDK does not recognize their type
        if base_kl_type in all_enums:
            cpp_cast_type = 'static_cast<%s>' % base_kl_type
            if '*' in cpp_type:
                cpp_cast_type = 'reinterpret_cast<%s*>' % base_kl_type
            autogen_param_name = '%s(%s)' % (cpp_cast_type, autogen_param_name)
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

# Get the name of the class, or '' if it should be ignored
def _class_name(struct_node):
    # should this element be ignored?
    name = struct_node.find('compoundname').text
    if (name in elementsToIgnore):
        return ''
    if name in opaque_type_wrappers:
        return ''
    return name

# Has this class been alias'ed to a KL type?  If so, we only
# want to output the alias, not the whole type    
def _class_alias(name):
    alias_type = name
    while alias_type in cpp_typedefs:
        alias_type = cpp_typedefs[alias_type]
    if alias_type in kl_type_aliases:
        return 'alias %s %s;\n' % (kl_type_aliases[alias_type], alias_type)

# test to see if this class/struct has any functions
# attached to it.  If it does (and there is no defined
# conversion function) we assume we will need to maintain
# a pointer to the native handle, and refer to this when
# calling functions
def _preprocess_class_or_struct_conversion(struct_node, kl_type):
    name = _class_name(struct_node)
    if not name:
        return

    if _class_alias(name):
        return

    has_functions = False
    for function in struct_node.iter('memberdef'):
        if function.get('kind') == 'function':
            has_functions = True
            autogen_class_typemapping.append(name)
            break

    if not name in json_codegen_typemapping:
        # Generate conversions for our classes.  This will
        # be virtually identical to the opaque wrappers
        conversion = _get_typemapping(name, name, has_functions)
        json_codegen_typemapping[name] = conversion


def _process_class_or_struct(struct_node, kl_type):
    name = _class_name(struct_node)
    if not name:
        return ''

    alias = _class_alias(name)
    if alias:
        return alias

    # begin defining our KL class.
    klLine = '';
    # first, find docs
    desc_node = struct_node.find('detaileddescription')
    if (desc_node != None):
        klLine = '/** {0}*/\n'.format(get_str(desc_node))

    # begin class
    klLine += kl_type + " " + name + " {\n"

    
    has_functions = name in autogen_class_typemapping
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
    for function in struct_node.iter('memberdef'):
        if function.get('kind') == 'function':
            klLine += process_function(function, name)

    print(klLine)
    return klLine + '//////////////////////////////////////////\n'

#
# Process a single class or struct (because the types are
# fairly interchangable in C++, either type can go to
# either a class or a struct in KL)
# 
def process_class_or_struct(struct_or_class_node, proccessing_fn):
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
                    return proccessing_fn(compound, 'struct')
                if (compound.attrib['kind'] == 'class'):
                    return proccessing_fn(compound, 'object')
    return ''

#
# Handle processing an XML file and writing out the
#
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

    # Put in overrides first, as these are things we can ensure are declared.
    file_contents += ["//////////////////////////////////////////////////\n//  overrides \n"]
    if override_name in custom_add_to_file:
        file_contents.append(custom_add_to_file[override_name] + '\n\n')

    # Always have class declarations at the top of the file
    file_contents += ["//////////////////////////////////////////////////\n//  classes \n"]

    # first we pre-process the classes to get their conversions
    # that is because we reference the conversions in class definitions,
    # and if classes are defined out-of-order (which is legitimate in C++)
    # we can generate incorrect C++ conversions in process_function
    for class_element in root.iter('innerclass'):
        process_class_or_struct(class_element, _preprocess_class_or_struct_conversion)
    for class_element in root.iter('innerclass'):
        file_contents.append(process_class_or_struct(class_element, _process_class_or_struct))

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
#
# Auto-generated conversion functions for easily-known types
#
def _generate_typemapping_header(full_json, filename, do_kl_type, to_fn_body, from_fn_body):
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

        # more String special case, we want all string types 
        # to map to String explicitly (no using alias command)
        alias_kl_type = kl_type_aliases.get(kl_type, kl_type)
        if alias_kl_type == 'String':
            kl_type = "String"

        if not do_kl_type(kl_type):
            continue

        
        if kl_type[-2:] == '[]':
            kl_type = 'VariableArray< Fabric::EDK::KL::%s >' % kl_type[:-2]
        elif kl_type[-2:] == '<>':
            kl_type = 'ExternalArray< Fabric::EDK::KL::%s >' % kl_type[:-2]


        cpp_type = val['ctype']
        sfrom = val['from']
        sto = val['to']
        
        _fn_body = from_fn_body
        if '%s' in _fn_body:
          _fn_body = from_fn_body % kl_type
        from_fn = ( 'inline bool %s(const Fabric::EDK::KL::%s & from, %s & to) { \n'
                    '  %s\n'
                    '  return true;\n'
                    '}\n\n' % (sfrom, kl_type, cpp_type, _fn_body))

        fh.write(from_fn)

        # When passing pointer values by-reference, we need
        # to const the reference in order for the cast to const
        # to succeed.
        # https://stackoverflow.com/questions/2908244/why-no-implicit-conversion-from-pointer-to-reference-to-const-pointer
        _fn_body = '' + to_fn_body
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


def do_pod(kl_type):
    # for all POD conversions we can simply do an equals
    kl_base_type = kl_type_aliases.get(kl_type, kl_type)
    return kl_base_type in kl_pod_types

def do_class(kl_type):
    # for auto-gen classes we know the full implementation
    return kl_type in autogen_class_typemapping

def do_opaque(kl_type):
    return kl_type in opaque_type_wrappers

def do_others(kl_type):
    return not(do_pod(kl_type) or do_class(kl_type) or do_opaque(kl_type))

def generate_typemapping_header(full_json):
    _generate_typemapping_header(full_json, '_typemapping_pod.h', do_pod, 'to = from;', 'to = from;')
    _generate_typemapping_header(full_json, '_typemapping_class.h', do_class, 'to->_handle = from;', 'to = reinterpret_cast<%s*>(from->_handle);')
    _generate_typemapping_header(full_json, '_typemapping_opaque.h', do_opaque, 'to._handle = from;', 'to = reinterpret_cast<%s*>(from._handle);')
    _generate_typemapping_header(full_json, '_typemapping.h', do_others, '#pragma message("Implement Me")', '#pragma message("Implement Me")')

########################################################################
# Write out a header file defining the entry-exit macros used by the kl2edk

def generate_define_header(full_json):
    fh = open(os.path.join(output_h_dir, '_defines.h'), 'w')

    fh.write(
    '/* \n'
    ' * This auto-generated file contains default macro definitions\n'
    ' * added to every call to/from the C++ functions in this module\n'
    ' *  - Do not modify this file, it will be overwritten\n'
    ' */\n\n\n#pragma once\n'
    ' \n'
    '#define %s(x)\n'
    '#define %s(x)\n'
    '#define %s(x, y) return _result;\n'  % (full_json['functionentry'], full_json['functionexit'], full_json['functionexitreturn'])
    )
########################################################################
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
        # we do not write an explicit alias for String's
        if kl_type == 'String':
            continue
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

########################################################################
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
        if not pf in fpm_enforced_order:
            f.write('    "' + pf + '",\n') 

    # For any custom KL files,
    # add them to the FPM list
    if custom_KL_dir:
        custom_files = glob.glob(custom_KL_dir + '/*.kl')
        for file in custom_files:
            filename = os.path.basename(file)
            if not filename in fpm_enforced_order:
                f.write('    "' + filename + '",\n')

    # Finally, add in the files in the enforced order
    # This can be used to ensure that files are added 
    # to the FPM appropriately
    for filename in fpm_enforced_order:
        f.write('    "' + filename + '",\n')

    f.write('  ]\n')
    f.write('}')

#
# Build a code-gen compatible type mapping from our typemapping
#
def _get_typemapping(c_type, kl_type, is_pointer):
    conversion = ( {
            'ctype': c_type,
            'from' : 'KL%s_to_CP%s' % (kl_type, c_type.replace('*', '')),
            'to' : 'CP%s_to_KL%s' % (c_type.replace('*', ''), kl_type),
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

        #conversion = _get_typemapping(cpp_raw_type, kl_raw_type, '*' in cpp_type)

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

    # auto-define the fn entry/exit points
    full_json["functionentry"] = parameter_prefix + "TRY_STATEMENT"
    full_json["functionexit"] = parameter_prefix + "CATCH_STATEMENT"
    full_json["functionexitreturn"] = parameter_prefix + "CATCH_STATEMENT_RETURN"


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
    final_codegen = generate_auto_codegen()
    
    # merge file is the users manually specified file
    final_file = os.path.join(output_dir, project_name + '.codegen.json')
    merge_file_path = os.path.join(root_dir, merge_codegen_file)
    if os.path.isfile(merge_file_path):

        with open(merge_file_path) as json_file:
            merge_codegen = json.load(json_file)
            final_codegen = jsonmerge.merge(final_codegen, merge_codegen)

    # generate a header file for conversion functions
    generate_typemapping_header(final_codegen)
    generate_define_header(final_codegen)

     # write out the result
    with open(final_file, 'w') as outfile:
        json.dump(final_codegen, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
        return final_codegen

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
json_codegen = generate_codegen()
