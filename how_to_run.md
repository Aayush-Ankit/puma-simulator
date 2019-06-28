# How to run  PUMA Compiler and Simulator

Below you will find some information on how to use the PUMA Compiler and Simulator.

| Requirement | Version                    |
| ----------- | -------------------------- |
| OS: Ubuntu  | 16.04.3 LTS (Xenial Xerus) |
| Python      | 2.7.12      


### 1. Create puma folder and change to the folder:
 ```
 mkdir puma
 cd puma
 ```
### 2. Setup PUMA Compiler:
```
git clone https://github.com/illinois-impact/puma-compiler
```
### 3. Setup PUMA Simulator:
```
git clone https://github.com/Aayush-Ankit/puma-simulator.git
git checkout training
```
#### 3.1 - Create virtual env using Python 2.7:
```
sudo apt-get install python-pip
sudo pip install virtualenv
virtualenv -p python2.7 .venv
```
#### 3.2 - Active virtual environment:
```
. .env/bin/activate
```
#### 3.3 - Install Puma Simulator dependencies:
```sh
pip install http://download.pytorch.org/whl/cu80/torch-0.3.0.post4-cp27-cp27mu-linux_x86_64.whl
pip install -r requirements.txt
```
If you are behind a proxy, you should type ```
pip --proxy $http_proxy install ...``` instead.

### 4. Go to the source Puma Compiler:

#### 4.1 - Clean compilation/emulation artifacts:
```
cd src/
make clean
```
#### 4.2 - Go to de /test and set up environment to point to libpuma.so:
```
cd test/
export LD_LIBRARY_PATH=`pwd`/../src:$LD_LIBRARY_PATH
```
#### 4.3 - Compile the examples:
```
make                           # Compile all examples
make <lstm-layer>.test       # Compile a specific example (make <example-name>.test)
```
#### 4.4 - Execute the examples to generate the PUMA assembly code:
```
./<lstm-model>.test          # Execute a specific example (./<example-name>.test)
```
### 5. Access the Puma Simulator test folder and copy the ```generate-py.sh``` file to compiler test folder where the ```.npy``` files are generated.

### 6. Update the SIMULATOR_PATH for the path to the Puma Simulator;

#### 6.1 - Execute and generate .npy archives:
```
./generate-py.sh
```
#### 6.2 - Copy the <example> folder that was generated and paste into the Puma Simulator:
```
cp -R large <PATH TO PUMA SIMULATOR>/puma-simulator/test/testasm/
```

#### 6.3 - Update in the ```config.py``` file (puma-simulator/include/) the number of tiles according to the quantity that was generated in your example model.
#### For example: Tiles generated from the ```lstm-layer.cpp``` model, a total of 25 tiles:
```
# Change here - Specify the Node parameters here
num_tile_compute = 23 # number of tiles mapped by dnn (leaving input and output tiles) -- (Line 85)

# Do not change this - total number of tiles
num_tile = num_node * num_tile_compute + 2 # +1 for first tile (I/O tile) - dummy, others - compute -- (Line 95)
```
### 7. Run your model, in this example, the ```lstm-layer.cpp```:
```
cd "PATH TO PUMA SIMULATOR"/src

python dpe.py -n lstm           
```

### 8. Then, you should see some results like:
```sh
...

('Cycle: ', 8783, 'Tile halt list', [1, 1, 0, 1])
('Cycle: ', 8784, 'Tile halt list', [1, 1, 0, 1])
('Cycle: ', 8785, 'Tile halt list', [1, 1, 0, 1])
('Cycle: ', 8786, 'Tile halt list', [1, 1, 1, 1])
cycle: 8786 Node Halted
Finally node halted | PS: max_cycles 10000
('Dumping tile num: ', 0)
('Dumping tile num: ', 1)
('Dumping tile num: ', 2)
('Dumping tile num: ', 3)
Output Tile dump finished
Success: Hadrware results compiled!!
```
### 9. The results for lstm model will be in the traces folder:
```
cd puma-simulator/test/traces/lstm
```
####  ```hardware_stats.txt```
```
Access and energy distribution of dynamic energy: 
Component                 num_access              percent
tile_control                5751403               0.60 %
edctrl                      405611                0.40 %
xbOutmem                    3112960               1.05 %
xbar_mtvm                   46464                 26.9 %
edram_bus                   411435                2.61 %
xbar_rd                     0                     0.0 %
xbar_op                     46336                 28.4 %
edram                       411435                7.48 %
xbar_mvm                    46464                 26.9 %
adc                         0                     0.0 %
imem_t                      752                   0.00 %
noc_inter                   0                     0.0 %
core_control                1156709               0.61 %
mux2                        11894784              0.0 %
mux1                        11894784              0.0 %
xbInmem_wr                  139264                0.04 %
alu_sna                     13381632              1.27 %
dac                         0                     0.0 %
noc_intra                   67642                 2.30 %
alu_mul                     6144                  0.00 %
snh                         11894784              0.00 %
xbar_wr                     0                     0.0 %
dmem                        798592                0.96 %
imem                        6812                  0.01 %
alu_act                     10240                 0.00 %
edctrl_counter              13824                 0.02 %
xbInmem_rd                  17408                 0.06 %
alu_other                   132096                0.07 %
alu_div                     0                     0.0 %
rbuff                       6528                  0.12 %

leakage_power: 633.54611067
node_area: 99.4071733152
leakage_energy: 2.06721891623e-05
tile_area: 0.443768888781
core_area: 0.0296594732947
dynamic_energy: 4.72800337861e-05
total_energy: 6.79522229484e-05
average_power: 960.686284315
time: 7.0733e-05
cycles: 70733
peak_power: 9551.59416329
network packet injection rate: 0.000274674783037
number of tiles mapped: 23
```
#### In the  archive```output.txt``` EDRAM contents will be saved.
