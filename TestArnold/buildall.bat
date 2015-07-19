
pushd "%~dp0"

REM Generate KL files from Doxygen XML output
if not exist GenKL mkdir GenKL
call python ../GenerateKL.py Fabric2Arnold.cfg.py

REM Generate C++ Files from KL files
if not exist ./GenCPP/h mkdir ./GenCPP/h
if not exist ./GenCPP/cpp mkdir ./GenCPP/cpp
kl2edk GenKL/Fabric2Arnold.fpm.json -o ./GenCPP/h -c ./GenCPP/cpp

popd
