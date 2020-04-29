set -v
set -e
path=`pwd` #path to your puma directory
echo $path
cppfile=conv-layer #name for cpp file that you want to compile ex- mlp_l4_mnist.cpp, conv-layer.cpp, convmax-layer.cpp
pumaenv=pumaenv #name for the environment 
#copying cnn config file
rm ${path}/puma-simulator/include/config.py #remove existing config file
cp ${path}/puma-simulator/include/example-configs/config-cnn.py  ${path}/puma-simulator/include/config.py #copy the mlp config file to include
#copying model file
rm ${path}/puma-compiler/test/conv-layer.cpp  
cp ${path}/puma-simulator/test/cnn/conv-layer-benchmark1.cpp  ${path}/puma-compiler/test/${cppfile}.cpp #copy the mlp config file to include 

cd ${path}/puma-compiler/src
source ~/.bashrc
conda activate ${pumaenv}

make clean
make

cd ${path}/puma-compiler/test
make clean
make ${cppfile}.test
export LD_LIBRARY_PATH=`pwd`/../src:$LD_LIBRARY_PATH
./${cppfile}.test 
echo $cppfile  
./generate-py.sh 
cp -r conv1 ../../puma-simulator/test/testasm

cd ${path}/puma-simulator/src


python dpe.py -n conv1



