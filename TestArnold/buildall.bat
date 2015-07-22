
pushd "%~dp0"

REM Generate KL files from Doxygen XML output
if not exist GenKL mkdir GenKL
call python ../GenerateKL.py Fabric2Arnold.cfg.py

REM Copy existing header in
copy _defines.h GenCPP\h

REM Generate C++ Files from KL files
if not exist GenCPP\h mkdir GenCPP\h
if not exist GenCPP\cpp mkdir GenCPP\cpp
del /Q GenCPP\cpp\*.*
kl2edk GenKL\Fabric2Arnold.fpm.json -o GenCPP\h -c GenCPP\cpp

REM Do any post-processing to get things as close as possible
call python ../MassageCPP.py Fabric2Arnold.cfg.py


popd
