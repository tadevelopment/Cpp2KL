import os
import glob
import shutil
from subprocess import call
import sys

# Pass in the cfg file of the extension to generate as an argument
if not len(sys.argv) > 1:
    print ("Usage - please pass the config file as an argument to this script")

cfg_file = sys.argv[1]

# import the configuration file.
execfile(cfg_file)
# Use cfg file as the root of further path manips
root_dir = os.path.dirname(cfg_file)
output_dir = os.path.join(root_dir, output_dir)
output_h_dir = os.path.join(root_dir, output_h_dir)
output_cpp_dir = os.path.join(root_dir, output_cpp_dir)
custom_cpp_dir = os.path.join(root_dir, custom_cpp_dir)
script_path = os.path.dirname(os.path.realpath(__file__))

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

# make these directories if necessary
ensure_dir(output_dir)
ensure_dir(output_h_dir)
ensure_dir(output_cpp_dir)

# remove all files in output directory
old_files = glob.glob(output_cpp_dir + '/*.cpp')
old_files += glob.glob(output_h_dir + '/*.h')
for file in old_files:
    os.remove(file)

# Generate our KL bindings
execfile(os.path.join(script_path, 'GenerateKL.py'))

# Copy existing header in
custom_files = glob.glob(custom_cpp_dir + '/*.h')
for file in custom_files:
    shutil.copy(file, output_h_dir)
custom_files = glob.glob(custom_cpp_dir + '/*.cpp')
for file in custom_files:
    shutil.copy(file, output_cpp_dir)

# Generate C++ Files from KL files
klcmd = 'kl2edk "%s/%s.fpm.json" -o "%s" -c "%s"' % (output_dir, project_name, output_h_dir, output_cpp_dir)
call(klcmd, shell=True)
#kl2edk GenKL\Fabric2Arnold.fpm.json -o GenCPP\h -c GenCPP\cpp

#REM Do any post-processing to get things as close as possible
execfile(os.path.join(script_path, 'MassageCPP.py'))
#call python ../MassageCPP.py Fabric2Arnold.cfg.py