import os
import glob
import shutil
from subprocess import call
import sys

# a small utility function to remove all brackets from a string
import re
def strip_brackets(str):
    return re.sub('[\[\](){}<>]', '', str)

# Pass in the cfg file of the extension to generate as an argument
if not len(sys.argv) > 1:
    print ("Usage - please pass the config file as an argument to this script")

cfg_file = sys.argv[1]
script_path = os.path.dirname(os.path.realpath(__file__))

# first, load our defaults, this will initialize all required variables
execfile(os.path.join(script_path, 'Defaults.cfg.py'))
# import the configuration file.
execfile(cfg_file)
# Use cfg file as the root of further path manips
root_dir = os.path.dirname(cfg_file)
output_dir = os.path.join(root_dir, output_dir)
output_h_dir = os.path.join(root_dir, output_h_dir)
output_cpp_dir = os.path.join(root_dir, output_cpp_dir)
if 'custom_cpp_dir' in globals():
    custom_cpp_dir = os.path.join(root_dir, custom_cpp_dir)
else:
    custom_cpp_dir = ''

if 'custom_KL_dir' in globals():
    custom_KL_dir = os.path.join(root_dir, custom_KL_dir)
else:
    custom_KL_dir = ''

print ('Custom CPP %s CustomKL %s' % (custom_cpp_dir, custom_KL_dir))


def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)

def copy_gen_file(f, out_dir):
    # If we would copy over a generated file, rename the generated file
    custom_filename = os.path.basename(f)
    custom_filename = os.path.join(out_dir, custom_filename)
    if os.path.isfile(custom_filename):
        rename_filename = custom_filename + '.gen'
        if os.path.isfile(rename_filename):
            os.remove(rename_filename)
        os.rename(custom_filename, rename_filename)

    shutil.copy(f, out_dir)

# make these directories if necessary
ensure_dir(output_dir)
ensure_dir(output_h_dir)
ensure_dir(output_cpp_dir)

# remove all files in output directory
old_files = glob.glob(output_cpp_dir + '/*.*')
old_files += glob.glob(output_h_dir + '/*.*')
for file in old_files:
    os.remove(file)

# Generate our KL bindings
execfile(os.path.join(script_path, 'GenerateKL.py'))

# Copy existing header in
if custom_cpp_dir:
    custom_files = glob.glob(custom_cpp_dir + '/*.h')
    for file in custom_files:
        copy_gen_file(file, output_h_dir)
    custom_files = glob.glob(custom_cpp_dir + '/*.cpp')
    for file in custom_files:
        copy_gen_file(file, output_cpp_dir)

if custom_KL_dir:
    custom_files = glob.glob(custom_KL_dir + '/*.kl')
    for file in custom_files:
        shutil.copy(file, output_dir)


# Generate C++ Files from KL files
klcmd = 'kl2edk "%s/%s.fpm.json" -o "%s" -c "%s"' % (output_dir, project_name, output_h_dir, output_cpp_dir)
if call(klcmd, shell=True) != 0:
    sys.exit("********************      kl2edk FAILURE         **************************")
#kl2edk GenKL\Fabric2Arnold.fpm.json -o GenCPP\h -c GenCPP\cpp

#REM Do any post-processing to get things as close as possible
execfile(os.path.join(script_path, 'MassageCPP.py'))
