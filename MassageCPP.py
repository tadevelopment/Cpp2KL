import glob
import re

# This file should be run on the post kl2edk code

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
        param_name = parameter_prefix + arg[1].capitalize()
        expr = r'\s*((.*) %s\b)(.*);' % param_name
        argm = re.search(expr, cpp_contents_fin)
        if not argm:
            print('warning: Aliased argument %s not found in %s' % (param_name,alias_fn))
            continue

        # replace the type declaration.  Also strip initializer
        alias_type = arg[0]
        cpp_contents_fin = cpp_contents_fin[:argm.start(2)] + ('%s %s' % (alias_type, param_name)) + cpp_contents_fin[argm.end(3):]
        # What is the conversion function for this type?
        # Find it and replace it with the correct type
        base_kl_type = kl_type_aliases[alias_type]
        if base_kl_type in json_codegen_typemapping:
          old_type_conv = json_codegen_typemapping[base_kl_type]['from']
          new_type_conv = json_codegen_typemapping.get(alias_type, {'from':'TYPE_ERROR'})['from']
          cpp_contents_fin = cpp_contents_fin.replace(old_type_conv, new_type_conv, 1)

      cpp_contents = cpp_contents_init + cpp_contents_fin

  # once done, write back
  with open(afile, 'w') as _file:
    _file.write(cpp_contents)

