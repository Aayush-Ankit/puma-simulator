set -v
set -e

cppfile=cnn9  # Enter name of cpp file. Also make sure this file exists in compiler/test/ 
path="$PWD/../../.."        

name=${cppfile}  #Name inside cpp file -- line 18

cd ${path}/puma-compiler/src

make clean
make

cd ${path}/puma-compiler/test
make clean
make ${cppfile}.test
export LD_LIBRARY_PATH=`pwd`/../src:$LD_LIBRARY_PATH
./${cppfile}.test 
rm -rf ${name}
./generate-py.sh
cp -r ${name} ../../puma-simulator/test/testasm

cd ${path}/puma-simulator/include

cp config/cnn-config.py ../config.py

cd ${path}/puma-simulator/src


python dpe.py -n ${name} 



