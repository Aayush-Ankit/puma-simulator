# This example instruction generation file shows writing instructions using JMP, BEQ, stride functionality for layer 1
# on IMA1_Tile1
# Also verfies EDRAM sharing between different IMAs
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
instrnpath = '/home/ankitaay/dpe/test/testasm/vgg11'
num_in = 4
num_rows = num_in
mp = 2
kernel = 3
num_out = (num_in-kernel+1)/mp # after max-pool
in_channel = 3
out_channel = 64
stride = 1
padding = 0

if not os.path.exists(instrnpath):
    os.makedirs(instrnpath)

## Generate input data for Tile 0
import random
random.seed(3)
inp_path = instrnpath + '/input.npy'
num_inputs = num_in*in_channel*num_rows
inp = {}
data = np.random.randn(num_inputs)
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
for i in range (in_channel*num_rows*num_in / (2*4*3)):
    target_tileId = '001'
    vtile_id = 0
    send_width = 4
    i_temp = i_send (i*4*3, vtile_id, send_width, target_tileId, vec = 3)
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
counter = 18
for i in range (in_channel * num_rows * (num_in + 2*padding) / (4*3)):
    if (padding > 0 and (((i % num_in) == 0) or ((i % num_in) == num_in-1))):
        neuron_id = -1 # for padding pixels
        i_temp = i_receive (i, neuron_id, counter)
    else:
        vtile_id = 1 if (i < 6/3) else 0
        receive_width = 4
        i_temp = i_receive (4*3*i, vtile_id, receive_width, counter, vec = 3)
    dict_list.append (i_temp.copy())

# Halt instruction in the end
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = temp_dir + '/tile_imem.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))


# Generate all other ima_imem.npy with halts for Tile 1
dict_temp = {}
dict_list = []
i_temp = i_hlt ()
dict_list.append (i_temp.copy())
for i in range (param.num_ima):
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

# Generate tile.imem.npy
dict_temp = {}
dict_list = []
# num_in = 224
# Send 3*4*224 input data - 3 channel, 4 rows, each row width 224
for i in range (in_channel*num_rows*num_in / 8):
    target_tileId = '001'
    vtile_id = 1
    send_width = 4
    i_temp = i_send (i*4, vtile_id, send_width, target_tileId, vec = 1)
    dict_list.append (i_temp.copy())

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

