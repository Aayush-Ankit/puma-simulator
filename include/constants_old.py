## This file contains the data structures used in differnet hierarchies.
## It also holds power, area and latency numbers of different component used in DPE design

# Limits the number of cycles an IMA runs in case it doesn't halt
cycles_max = 50000 # Put both these to very large numbers (when design is bug-free)!
infinity = 100000
debug = 1 #if 0, no traces or memsim will be generated for compute tiles

##################################################
## Technology/Other constants for all the modules
##################################################
# using fixed point binary (n bits, m (<= n) for integral part)
num_bits = 16
int_bits = 4
frac_bits = num_bits - int_bits

# IMA
vdd = 0.9
xbar_out_min = -10e-10
xbar_out_max = 1 # think about this - ???

########################################
## Define commonly used data structures
########################################
# List of supported opcodes for tile
op_list_tile = ['send', 'receive', 'compute', 'halt']

# Instruction format for Tile
dummy_instrn_tile = {'opcode' : op_list_tile[0],
                     'mem_addr': 0,     # send/receive - edram_addr
                     'r1': 0,     # send-send_width, receive-receive_width
                     'r2': 0,     # send-target_addr, receive-counter
                     'vtile_id': 0, # send/receive-neuron_id
                     'ima_nma': '',      # compute - a bit for each ima
                     'vec': 0} # vector width

# List of supported opcodes/aluops for IMA - cp will copy data (from data memory of ima to xbarInmem)
op_list = ['ld', 'cp', 'st', 'set', 'nop', 'alu', 'alui', 'mvm', 'hlt', 'jmp', 'beq', 'alu_int']
aluop_list = ['add', 'sub', 'sna', 'mul', 'sigmoid'] # sna is also used by mvm isntruction

# Instruction format for IMA
dummy_instrn = {'opcode' : op_list[0],      # instrn op
               'aluop'  : aluop_list[0],   # alu function
               'd1'     : 0,               # destination
               'r1'     : 0,               # operand1 (stride for mvm)
               'r2'     : 0,               # operand2
               'r3'     : 0,               # operand3 (shift)
               'vec'    : 0,               # vector width
               'imm'    : 0,               # immediate (scalar) data
               'xb_nma' : 0 }              # xbar negative-mask, a xbar evaluates if neg-mask = 1

# List of pipeline stages - in order for IMA
stage_list = ['fet', 'dec', 'ex']
last_stage = 'ex'

#################################################
# DPE Hardware Configuration Parameters
#################################################

#################################################
# IMA Hierarchy
    # Number of Xbars
    # Crossbar Size
    # Bit resolution of ADCs and DACs
    # Number of ADCs
    # Number of ALUs
    # Data memory, Xbar in/out memory (Register) & Instruction memory sizes
#################################################

# Enter parameters here:
num_xbar = 8
xbar_bits = 2
xbar_size = 128
dac_res = 1
adc_res = 16
num_adc = 8
num_ALU = 1
dataMem_size = 256
instrnMem_size = 10000
data_width = num_bits # (microarchitecture param)
xbdata_width = data_width # (nn speciic for now)

# Enter IMA component latency
xbar_lat = 2
dac_lat = 0
adc_lat = 0
snh_lat = 0
mux_lat = 0
alu_lat = 0
mem_lat = 1
# Added here for simplicity now (***needs modification later***)
memInterface_lat = infinity # infinite latency

#################################################
# Tile Hierarchy
    # Number of IMAs
    # EDRAM size
    # Shared Bus width
    # Instruction memory size
    # Receive Buffer size
#################################################

# Enter parameters here:
num_ima = 12
#edram_buswidth = 16
edram_buswidth = 1*data_width
edram_size = 10000
receive_buffer_depth = 16 # number of edram buffer entries (each entry maps to a virtual input tile)
receive_buffer_width =  384/num_bits # size of receive buffeer entry (in terms of number of neurons)

# Enter component latency
tile_instrnMem_size = 200
edram_lat = 2
receive_buffer_lat = 0

################################################
# Node Hierarchy
    # Number of Tiles
    # NOC - Topology (Currently assumes a cmesh (c=4, same as ISSAC))
        # n = number of dimension\
        # k = number of tiles in each dimension
        # c = concentartion (tiles/router)
        # average injection rate (0.25 - a tile injects a new packet for each destination in every four cycles)
################################################

# Enter parameters here:
num_tile_compute = 1
# cmesh topology
n = 2
k = 4
c = 4
inj_rate = 0.01
# addressing tiles (in and outside node)
num_bits_nodeId = 1 # can have upto 2 nodes
num_bits_tileId = 2 # can have upto 4 num_tile (**see bottom of this file**) in a node

# Enter component latency (Based on teh above NOC topological parameters)
noc_latency_intranode = 1
noc_latency_internode = 2

# Do not change this
num_tile = num_tile_compute + 2 # +2 for first & last tiles - dummy, others - compute
