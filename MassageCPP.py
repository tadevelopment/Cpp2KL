import glob
import sys
import os

cfg_file = sys.argv[1]
# import the configuration file.
execfile(cfg_file)

# Use cfg file as the root of further path manips
root_dir = os.path.dirname(cfg_file)
output_dir = os.path.join(root_dir, output_dir)
output_h_dir = os.path.join(root_dir, output_h_dir)
output_cpp_dir = os.path.join(root_dir, output_cpp_dir)

# This file should be run on the post kl2edk code

# So far, the only thing we can do is to try to fix
# the missing return statements.  We guess 0 for any return type
for afile in glob.glob(output_cpp_dir + '/*.cpp'):
  cpp_contents = ''
  with open(afile, 'r') as _file:
    cpp_contents = _file.read()

  cpp_contents = cpp_contents.replace('return ;', 'return 0;')
  # once done, write back
  with open(afile, 'w') as _file:
    _file.write(cpp_contents)

