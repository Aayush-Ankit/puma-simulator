## This file contains the configurable parameters in DPE (all hierarchies - IMA, Tile, Node)
## All user specified parameters are provided by this file only

## Debug - 0 (1): dpe simulation will (won't) produce ima/tile traces while simulating
cycles_max = 5000000 # Put both these to very large numbers (when design is bug-free)!
debug = 1
xbar_record = 1

## Operand precision (fixed point allowed only): num_bits = int_bits + frac_bits
num_bits = 16
int_bits = 4
frac_bits = num_bits - int_bits

## IMA configurable parameters (permissible values for each parameter provided here)
## Instruction generation - affected by xbar_bits, num_xbar, xbar_size.
# xbar_bits: 2, 4, 6
# num_xbar: positive integer
# xbar_size: 32, 64, 128, 256
# dac_res: positive integer <= num_bits
# adc_res: positive integer <= num_bits
# num_adc: positive integer <= num_xbar (doesn't allow more than one ADC per xbar)
# num_ALU: positive integer
# dataMem_size: (in Bytes) - 256, 512, 1024, 2048 (affects instrn width, hence capped)
# instrnMem_size: (in Bytes) - 512, 1024, 2048

# Fixed parameters
data_width = num_bits # (in bits)
xbdata_width = data_width # (in bits)
instrn_width = 48 # (in bits)

# Change here - Specify the IMA parameters here
xbar_bits = 2
num_matrix = 2 # each matrix is 8-fw xbars, 8-bw xbars and 16-delta xbars
xbar_size = 128
dac_res = 1
adc_res = 8
num_adc = 2 * num_matrix
num_ALU = num_matrix*2
#dataMem_size = num_matrix*(6*xbar_size) # 4 for 4 input spaces within matrix (1 for f/b each, 2 for d)
dataMem_size = 2048 # 2048 is larger than num_matrix*(6*xbar_size)
instrnMem_size = 512 #in entries

# This depends on above parameters
datamem_off = xbar_size * (num_matrix*6) # each matrix has 6 memory spaces (1 for f/b, 2 for d)
phy2log_ratio = num_bits / xbar_bits # ratio of physical to logical xbar
lr = 0.25 # learning rate for updates to d-xbar

## Tile configurable parameters (permissible values for each parameter provided here)
## Instruction generation - affected by num_ima
# num_ima: positive integer
# edram buswidth: positive integer <= 16 (actual buswidth - this integer*data_width)
# edram_size: (in KiloBytes) - 64, 128, 256, 512
# receive_buffer_depth: 4, 8, 12, 16, 32 (number of edram buffer entries (each entry maps to a virtual tile)) \
#        puts a cap on the maximum num ber of tiles that can send data to a tile in next layer
# receive_buffer_width: edram_buswidth/data_width (Fixed - in terms of number of neurons)
# tile_instrnMem_size: 256, 512, 1024 (in Bytes)

# Fixed parameters
instrn_width = 48 # bits (op-2, vtile_id-6, send/receive_width-8, target_addr/counter-16, vw-8, mem_addr-16)
edram_buswidth = 256 # in bits
#receive_buffer_depth = 16
receive_buffer_depth = 150 #set equal to num_tile_max
receive_buffer_width =  edram_buswidth / num_bits # size of receive buffeer entry (in terms of number of neurons)

# Change here - Specify the Tile parameters here
num_ima = 8
edram_size = 64 # in Kilobytes (64 KB - same as issac)
tile_instrnMem_size = 2048 # in entries

## Node configurable parameters (permissible values for each parameter provided here)
## Instruction generation - affected by num_tile
# num_tile_compute: positive integer
# inj_rate < 0.2 (depends on the mapping)
# num_port: 4, 8

# Fixed parameters
# NOC topology: cmesh (n=2, k=4, c=4) - can fit k*n*c tiles
cmesh_c = 4
num_bits_tileId = 32
flit_width = 32
packet_width = edram_buswidth/data_width #in multiples of flits (data considered only - booksim consider address itself)
# (b bit of address = logN, N is the number of nodes)

# Change here - Specify the Node parameters here
num_tile_compute = 5 # number of tiles mapped by dnn (leaving input and output tiles)
num_tile_max = 168.0 # maximum number of tiles per node
num_inj_max = num_tile_max # [conservative] max number of packet injections that can occur in a cycle (each tile injects a packet into NOC each cycle)
noc_inj_rate = 0.005
noc_num_port = 4

## Node parameters - Our way of simulation just assumes all tile in one actual node
num_node = 1

# Do not change this - total number of tiles
num_tile = num_node * num_tile_compute + 2 # +1 for first tile (I/O tile) - dummy, others - compute

