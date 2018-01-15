# Converts vgg11 to dpe ISA (tile and IMA instructions)
import sys, os
import numpy as np
import models
import torch
import math

sys.path.insert (0, '/home/ankitaay/dpe/include/')
sys.path.insert (0, '/home/ankitaay/dpe/src/')
import constants as param

# import the data_convert module (float to fixed conversions)
from data_convert import *
from instrn_proto import *
from tile_instrn_proto import *

#*****************************************************************************************************************
## Rules to map a conv layer (for now!) - (**produces one output neuron of all outpur maps at once)
# 1. each xbar column maps a different output (no input repetition)
# 2. for output/num_output_maps (per output column) larger than xbar_size, map them across different xbars (x-axis)
# 3. for input size (reqd. for one output)larger than xbar_size, map them across multiple xbars (y-axis)
# 4. for weight precision larger than xbar bits map, the weight bits across multiple xbars (z-axis)

## Rules for xbar replication (for now!)
# 1. produce multiple output neurons  (adjacent ones from same output map) simultaneously

## Think of ways to use input sharing between strides - can lead to energy savings
# 1. Repeated within xb_inmem movements - use xb_inmem movements for computing with different strides
# 2. Muxed conenction to DAC input from xb_inmem

#*****************************************************************************************************************
# Load the DNN model
'''torch.manual_seed (1)
net = models.vgg11()

## generate vxbars from feature list in vgg11:
layer_list = [0, 3, 6, 8, 11, 13, 16, 18]
vxbar_list = []

for layer in layer_list:
    l = net.features[layer]
    kernel_size = l.kernel_size
    in_channels = l.in_channels
    out_channels = l.out_channels

    # map to a virtual xbar - each xpoint is full weight (eg: 16 bit weights)
    numIn_vxbar = in_channels * kernel_size[0] * kernel_size[1] # num of virtual inputs to xbar
    numOut_vxbar = out_channels # number of virtual outputs from xbar
    wt = l.weight.data.numpy()
    vxbar_temp = np.zeros ((numIn_vxbar, numOut_vxbar), dtype=float)
    for i in range (numOut_vxbar):
        vxbar_temp[:,i] = wt [i,:,:,:].reshape(numIn_vxbar)
    vxbar_list.append (vxbar_temp)


# Analyzed the formed vxbar(s)
print ('See size of formed virtual xbars')
for vxbar in vxbar_list:
    print (np.shape(vxbar))

#*****************************************************************************************************************
## Produce actual xbar weights file based on above xbar params (bits & size)
# each list entry is a wtfile list for one vxbar
wtfile_list = [[] for i in range(len(vxbar_list))] # A list of (list of dictionaries)

# hw parameters that will affect mapping (in terms of number of xbars needed)
wt_bits = param.num_bits # 16
xbar_bits = param.xbar_bits # 2
xbar_size = param.xbar_size # 128

for i in range (len(vxbar_list)):  # x: output, y: input, z: weight
    # axes traversal pattern: z >> x >> y
    [inp_size, out_size] = np.shape (vxbar_list[i])
    for j in range (int(math.ceil(float(out_size)/xbar_size))): # output
        for k in range (int(math.ceil(float(inp_size)/xbar_size))): # input
            col_end = min ((j+1)*xbar_size-1, out_size)
            row_end = min ((k+1)*xbar_size-1, inp_size)
            temp_wtfile  = vxbar_list[i][k*xbar_size:row_end+1, j*xbar_size:col_end+1]
            temp_wtfile_fixed  = float2fixed_2d (temp_wtfile, param.int_bits, param.frac_bits)
            for l in range (wt_bits/xbar_bits): # weight
                temp_wtfile_name = 'out' + str (j) + 'inp' + str (k) + 'wt' + str (l)
                temp_xbar_val = getBitsFromList (temp_wtfile_fixed, l*xbar_bits, xbar_bits) #matrix, start_bits, num_bits
                temp_xbar_val_float = fixed2float_2d (temp_xbar_val, param.int_bits, param.frac_bits)
                temp_dict = {'name':temp_wtfile_name, 'xbar_val':temp_xbar_val_float}
                wtfile_list[i].append(temp_dict)

# Saving to save time in processing again n again
np.save ('wtfile_list.npy', wtfile_list)

# Analyzed the formed xbar_files
wtfile_list = np.load ('wtfile_list.npy')
print ('See the number of xbar wt files (program files) generated for each feature layer')
for wtfile in wtfile_list:
    print (len(wtfile))

#*****************************************************************************************************************
## Rules for organizing xbars in tiles and ima based on num_xbar (in ima), num_ima (in tile)
# 1. Each ima maps to one layer only (even if xbars in ima remain unutilized)
# 2. Placement of xbars in imas is focussed to exploit input sharing (Other option: Output Sharing)
# 3. No xbar replication (replication can lead to improved throughput) (Other option: replicate to produce multiple
# ouputs from in an putput map in parallel)

num_xbar = 8
num_ima = 12'''

#*****************************************************************************************************************
instrnpath = '/home/ankitaay/dpe/test/testasm/vgg11'
num_in = 4
num_rows = 4
num_out = 112 # after max-pool
in_channel = 3
out_channel = 64
kernel = 3
stride = 1
padding = 0
mp = 2


if not os.path.exists(instrnpath):
    os.makedirs(instrnpath)

## Generate input data for Tile 0
inp_path = instrnpath + '/input.npy'
num_inputs = num_in*in_channel*num_rows
inp = {}
data = np.random.rand(num_inputs)
counter = np.ones (num_inputs)
valid = np.ones (num_inputs)
inp = {'data':data, 'counter': counter, 'valid':valid}
np.save (inp_path, inp)


## Generate instruction for Tile 0 (dummy tile)
temp_dir = instrnpath + '/tile0'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Generate tile.imem.npy
dict_temp = {}
dict_list = []
# num_in = 224
# Send 3*4*224 input data - 3 channel, 4 rows, each row width 224
for i in range (in_channel*num_rows*num_in):
    target_tileId = '001'
    i_temp = i_send (i, i, target_tileId)
    dict_list.append (i_temp.copy())

# Halt instruction in the end
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = temp_dir + '/tile_imem.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))

# Generate all ima_imem.npy with halts for Tile 0
dict_temp = {}
dict_list = []
i_temp = i_hlt ()
dict_list.append (i_temp.copy())
for i in range (param.num_ima):
    filename = temp_dir + '/ima_imem' + str(i) + '.npy'
    print (filename + ' generated')
    np.save(filename, dict_list)
    print ('Total no of instructions: ', len(dict_list))


## Generate instruction for Tile 1 (compute tile)
temp_dir = instrnpath + '/tile1'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Generate tile.imem.npy - way how data read from edram is buffered into IMA and provided to xbar may enhance input
# sharing  and lead to energy/performance improvements
# Process convolution layer
dict_temp = {}
dict_list = []

#Receive 3 intermediate rows (ignoring the first row - padding)
# Receive 3*2*226 (3 channels, 2 rows, 224 row size + 2 for padding (1,1)
nId = 0 # neuronId
counter = 6
for i in range (in_channel * num_rows * (num_in + 2*padding)):
    if (padding > 0 and (((i % num_in) == 0) or ((i % num_in) == num_in-1))):
        neuron_id = -1 # for padding pixels
        i_temp = i_receive (i, neuron_id, counter)
    else:
        i_temp = i_receive (i, nId, counter)
        nId += 1
    dict_list.append (i_temp.copy())

# initiate the imas to compute
i_temp = i_compute ('1' * param.num_ima)
dict_list.append (i_temp.copy())

# Halt instruction in the end
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = temp_dir + '/tile_imem.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))

# Generate ima_imem0.npy for Tile 1 - (LD, MVM, ST) - compute 2 rows of output - MaxPool
# Assumes depth-major data layout (dept -> row -> column)
dict_temp = {}
dict_list = []
out_addr = num_rows * num_in * in_channel
datamem_off = param.num_xbar*param.xbar_size

for h in range (num_rows-kernel+1):
    # A set of convolution to produce first row of relu output, all output maps
    # i corresponds to ith convolution
    for i in range (num_in + 2*padding - kernel + 1):
        # j correponds to the jth value fetched within 1 convolution
        for j in range (kernel):
            for k in range (in_channel*kernel): # kernel - kernel_size
                addr = h*(in_channel*num_in) + (i*in_channel) + j*in_channel*num_in + k
                d1 = j*in_channel*kernel + k
                i_temp = i_load (d1, addr)
                dict_list.append (i_temp.copy())

        # copy the input values to all xbInmem
        for j in range (param.num_xbar):
            for k in range (kernel*kernel*in_channel):
                r1 = k #source is first xbar
                d1 = j*param.xbar_size + k
                i_temp = i_copy (d1, r1)
                dict_list.append (i_temp.copy())

        # MVM to compute in all 8 xbars
        #stride_val = in_channel * kernel * stride
        stride_val = 0
        i_temp = i_mvm (8, stride_val)
        dict_list.append (i_temp.copy())

        # Shift and add outputs of all crossbar to produce final output
        '''for j in range (1, param.num_xbar):
            for k in range (out_channel):
                # For shift and add - add a third operand to ALU ??
                i_temp = i_alu ('sna', k, k, j*param.xbar_size + k)
                dict_list.append (i_temp.copy())'''

        # Do Relu and store a row of output in datamemory
        for j in range (out_channel):
            i_temp = i_alu ('relu', datamem_off+j, j)
            dict_list.append (i_temp.copy())

        # For avery alternate column
        if (i % mp == 1):
            # Do a max (half-max) for adjacent convolution outputs (same output map)
            for j in range (out_channel):
                i_temp = i_alu ('max', datamem_off+j, j, datamem_off+j)
                dict_list.append (i_temp.copy())

            # Do a max with previous value row value for this channel (if applicable)
            if (h % mp == 1):
                for j in range (out_channel):
                    addr = out_addr + (i/2)*out_channel + j
                    i_temp = i_load (datamem_off+out_channel+j, addr)
                    dict_list.append (i_temp.copy())
                    i_temp = i_alu ('max', datamem_off+j, datamem_off+j, datamem_off+out_channel+j)
                    dict_list.append (i_temp.copy())

            # Store back the data (either half max, or full max)
            for j in range (out_channel):
                counter = 1
                addr = out_addr + (h/4)*num_out + (i/2)*out_channel + j
                i_temp = i_store (datamem_off+j, addr, counter)
                dict_list.append (i_temp.copy())

i_temp = i_hlt ()
dict_list.append (i_temp.copy())
filename = temp_dir + '/ima_imem' + str(0) + '.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))

# Generate all other ima_imem.npy with halts for Tile 1
dict_temp = {}
dict_list = []
i_temp = i_hlt ()
dict_list.append (i_temp.copy())
for i in range (1,param.num_ima):
    filename = temp_dir + '/ima_imem' + str(i) + '.npy'
    print (filename + ' generated')
    np.save(filename, dict_list)
    print ('Total no of instructions: ', len(dict_list))


## Generate instruction for Tile 2 (dummy tile)
temp_dir = instrnpath + '/tile2'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Generate tile.imem.npy
dict_temp = {}
dict_list = []

# Halt instruction in the end
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = temp_dir + '/tile_imem.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))

# Generate all ima_imem.npy with halts for Tile 2
dict_temp = {}
dict_list = []
i_temp = i_hlt ()
dict_list.append (i_temp.copy())
for i in range (param.num_ima):
    filename = temp_dir + '/ima_imem' + str(i) + '.npy'
    print (filename + ' generated')
    np.save(filename, dict_list)
    print ('Total no of instructions: ', len(dict_list))

