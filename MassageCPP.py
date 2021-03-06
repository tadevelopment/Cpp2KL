import glob
import re

# This file should be run on the post kl2edk code
fn_exit = json_codegen['functionexit']

remove_def_comments = re.compile("^// Defined at.*$\n", re.MULTILINE)

# So far, the only thing we can do is to try to fix
# the missing return statements.  We guess 0 for any return type
for afile in glob.glob(output_cpp_dir + '/*.cpp'):
  cpp_contents = ''
  with open(afile, 'r') as _file:
    cpp_contents = _file.read()

  cpp_contents = cpp_contents.replace('return ;', 'return 0;')

  # Unfortunately, kl2edk does not handle alias'es.  If a parameter
  # is an alias, that is because that type may be overloaded (eg
  # multiple C++ types mapping to a single KL type). We use aliasing
  # to signal which is the correct C++ type to convert to.
  # kl2edk ignores  this type information, and will convert from the base
  # KL type to a single C++ type.
  # To compensate for this, we manually search out the affected
  # functions and add the correct type mapping
  for alias_fn, fn_args in functions_with_aliases.iteritems():
    # Is this function in this file?
    m = re.search(r'\b%s\b' % alias_fn, cpp_contents)
    if m:
      fn_start = m.start()
      cpp_contents_init = cpp_contents[:fn_start]
      cpp_contents_fin = cpp_contents[fn_start:]
      
      # Replace current target types
      for arg in fn_args:
        fn_return_idx = cpp_contents_fin.find(fn_exit)
        param_name = _param_name(arg[1])
        expr = r'\s*((.*) %s\b)(.*);' % param_name
        argm = re.search(expr, cpp_contents_fin)
        if not argm or argm.start() > fn_return_idx:
            print('warning: Aliased argument %s not found in %s' % (param_name,alias_fn))
            continue

        alias_type = arg[0]
        if alias_type not in kl_type_aliases:
            # This will happen if we have recorded an alias function
            # for an array - the alias is different because of the brackets
            base_alias_type = strip_brackets(alias_type)
            base_kl_type = kl_type_aliases[base_alias_type]
            # in this instance kl2edk will fail to generate the param conversion
            # so we just insert it ourselves
            typemapping = json_codegen_typemapping.get(alias_type)
            conversion = "\n".join((
                "",
                "  %s %s;" % (typemapping['ctype'], param_name),
                "  if(!%s(%s, %s)) { " % (typemapping['from'], arg[1], param_name),
                "    setError(\"Error in %s. unable to convert: %s\");" % (alias_fn, param_name),
                "  }"
            ))
            cpp_contents_fin = cpp_contents_fin[:argm.start()] + conversion + cpp_contents_fin[argm.start():]
            
        else:
            # replace the type declaration.  Also strip initializer
            cpp_contents_fin = cpp_contents_fin[:argm.start(2)] + ('%s %s' % (alias_type, param_name)) + cpp_contents_fin[argm.end(3):]
            fn_return_idx = cpp_contents_fin.find(fn_exit)

            # What is the conversion function for this type?
            # Find it and replace it with the correct type
            base_kl_type = kl_type_aliases[alias_type]
            if base_kl_type in json_codegen_typemapping:
              old_type_conv = json_codegen_typemapping[base_kl_type]
              new_type_conv = json_codegen_typemapping.get(alias_type, {'from':'TYPE_ERROR'})
              conv_idx = cpp_contents_fin.find(old_type_conv['from'], 0, fn_return_idx)
              if conv_idx > 0:
                cpp_contents_fin = cpp_contents_fin.replace(old_type_conv['from'], new_type_conv['from'], 1)

              # if the element is returned, then we will need to replace the return as well
              conv_idx = cpp_contents_fin.find(old_type_conv['to'] + '(' + param_name, 0, fn_return_idx)
              if conv_idx > 0:
                  cpp_contents_fin = cpp_contents_fin.replace(old_type_conv['to'], new_type_conv['to'], 1)

      cpp_contents = cpp_contents_init + cpp_contents_fin

  # Get rid of that super-annoying message telling us where a function is defined
  # Those lines change every time we re-compile and make it difficult to see
  # down where actual changes have occured in Git
  cpp_contents = remove_def_comments.sub("", cpp_contents)

  # once done, write back
  with open(afile, 'w') as _file:
    _file.write(cpp_contents)

# Strip all junk messages from headers as well
for afile in glob.glob(output_h_dir + '/*.h'):
  h_contents = ''
  with open(afile, 'r') as _file:
    h_contents = _file.read()
  h_contents = remove_def_comments.sub("", h_contents)
  with open(afile, 'w') as _file:
    _file.write(h_contents)
