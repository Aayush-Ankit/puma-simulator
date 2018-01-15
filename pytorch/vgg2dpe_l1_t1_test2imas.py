# This example instruction generation file shows writing instructions using JMP, BEQ, stride functionality for layer 1
# on IMA1_Tile1. Subsequently relicates layer 1 code on IMA2_Tile with different store address to verify
# EDRAM sharing between different IMAs.

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
counter = 18
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

## Initialization
# set row_max & col_max
row_max = int2bin(num_rows-kernel, 16) # 0 - num_rows-kernel (total - num_rows-kernel+1)
col_max = int2bin(num_in-kernel, 16)
i_temp = i_set (datamem_off, row_max)
dict_list.append (i_temp.copy())
i_temp = i_set (datamem_off+1, col_max)
dict_list.append (i_temp.copy())

# set row_cur & col_cur (current output row or column being computed)
row_cur = int2bin(0, 16)
col_cur = int2bin(0, 16)
i_temp = i_set (datamem_off+2, row_cur)
dict_list.append (i_temp.copy())
i_temp = i_set (datamem_off+3, col_cur)
dict_list.append (i_temp.copy())

edram_rowmax = int2bin(3, 16) # number of rows of input image edram can hold
i_temp = i_set (datamem_off+4, edram_rowmax)
dict_list.append (i_temp.copy())

num_val = int2bin(in_channel * num_in, 16) # number of inputs image pixels per row of edram (num_in * in_channel)
i_temp = i_set (datamem_off+5, num_val)
dict_list.append (i_temp.copy())

num_val = int2bin(in_channel, 16) # number of in_channels
i_temp = i_set (datamem_off+6, num_val)
dict_list.append (i_temp.copy())

## Set the max pool window size and a one for comparison (for odd row/col)
mp = int2bin(2, 16) # max-pool window size
i_temp = i_set (datamem_off+10, mp)
dict_list.append (i_temp.copy())

one = int2bin(1, 16) # one for comparison
i_temp = i_set (datamem_off+11, one)
dict_list.append (i_temp.copy())

## Set the output addr affset
out_addr_off = int2bin(kernel*num_in*num_rows + 4, 16)
i_temp = i_set (datamem_off+12, out_addr_off)
dict_list.append (i_temp.copy())

## Set the numout we will compute per row of output map (after max-pool) and out_channel
num_val_out = int2bin(num_out*out_channel, 16)
i_temp = i_set (datamem_off+15, num_val_out)
dict_list.append (i_temp.copy())

num_out_channel = int2bin(out_channel, 16)
i_temp = i_set (datamem_off+16, num_out_channel)
dict_list.append (i_temp.copy())

l1_pc = len(dict_list)
## l1_pc - compute the load addresses for 3 loads (3 rows) based on row_cur & col_cur
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('mod', datamem_off+7, datamem_off+2, datamem_off+4) # first row
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('mul', datamem_off+7, datamem_off+7, datamem_off+5) # (row_curr % 3)*(in_channel*col_max)
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('mul', datamem_off+8, datamem_off+3, datamem_off+6) # col_curr * in_channel
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('add', datamem_off+7, datamem_off+7, datamem_off+8)
dict_list.append (i_temp.copy())

i_temp = i_alu_int ('add', datamem_off+8, datamem_off+7, datamem_off+5) # second row
dict_list.append (i_temp.copy())

i_temp = i_alu_int ('add', datamem_off+9, datamem_off+8, datamem_off+5) # third row
dict_list.append (i_temp.copy())

## load the three rows (each load loads kernel*in_channel values)
vw = kernel*in_channel
for j in range (kernel):
    i_temp = i_load (j*in_channel*kernel, datamem_off+7+j, vw)
    dict_list.append (i_temp.copy())

## copy the values to all 8 xbars (input-sharing)
vw = in_channel * kernel * kernel
for j in range (1,param.num_xbar):
    i_temp = i_copy (j*param.xbar_size, 0, vw)
    dict_list.append (i_temp.copy())

## mvm not using stride support in xbar_inmemstride_val1 = 3
i_temp = i_mvm (8, 0, 0)
dict_list.append (i_temp.copy())

## Check if computing odd col/row
i_temp = i_alu_int ('mod', datamem_off+13, datamem_off+2, datamem_off+10) # check for odd row
dict_list.append (i_temp.copy())

i_temp = i_alu_int ('mod', datamem_off+14, datamem_off+3, datamem_off+10) # check for odd col
dict_list.append (i_temp.copy())

l2_pc = len(dict_list) + param.num_xbar-1 + 3
i_temp = i_beq (datamem_off+14, datamem_off+11, l2_pc)
dict_list.append (i_temp.copy())

## Compute output of conv (shift and add) and relu for even column
vw = out_channel
for j in range (1,param.num_xbar):
    i_temp = i_alu ('sna', datamem_off+20, 0, j*param.xbar_size, j*param.xbar_bits, vec = vw)
    dict_list.append (i_temp.copy())

i_temp = i_alu ('relu', datamem_off+20, datamem_off+20, vec = vw)
dict_list.append (i_temp.copy())

l3_pc = len(dict_list) + param.num_xbar-1 + 15
i_temp = i_jmp (l3_pc)
dict_list.append (i_temp.copy())

## l2_pc - branch target - odd column - conv, relu, half-max
vw = out_channel
for j in range (1,param.num_xbar):
    i_temp = i_alu ('sna', datamem_off+20+out_channel, 0, j*param.xbar_size, j*param.xbar_bits, vec = vw)
    dict_list.append (i_temp.copy())

i_temp = i_alu ('relu', datamem_off+20+out_channel, datamem_off+20+out_channel, vec = vw)
dict_list.append (i_temp.copy())

i_temp = i_alu ('max', datamem_off+20, datamem_off+20, datamem_off+20+out_channel, vec = vw)
dict_list.append (i_temp.copy())

## l4_pc - store the half-max (even row) / full-max value (odd row)
# set the out_addr where output in case of (odd col) gets stored
i_temp = i_alu_int ('div', datamem_off+17, datamem_off+2, datamem_off+10) #row_curr/mp
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('mul', datamem_off+17, datamem_off+17, datamem_off+15) #(row_cur/mp)*(num_out*out_channel)
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('div', datamem_off+18, datamem_off+3, datamem_off+10) #col_cur/mp
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('mul', datamem_off+18, datamem_off+18, datamem_off+16) #(col_cur/mp) * out_channel
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('add', datamem_off+17, datamem_off+17, datamem_off+18) #(row_cur/mp)*(num_out*out_channel) + (col_cur/mp)*(out_channel)
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('add', datamem_off+17, datamem_off+17, datamem_off+12) #out_addr_off + row_cur/mp*num_out + col_cur/mp
dict_list.append (i_temp.copy())

## branch if odd row
l4_pc = len(dict_list) + 3
i_temp = i_beq (datamem_off+13, datamem_off+11, l4_pc)
dict_list.append (i_temp.copy())

i_temp = i_store (datamem_off+17, datamem_off+20, counter = 1, vec = out_channel) # even row
dict_list.append (i_temp.copy())

l5_pc = len(dict_list) + 4
i_temp = i_jmp (l5_pc) # increment col_cur & row_cur
dict_list.append (i_temp.copy())

## l4_pc - odd row - load prev row, do another halt-max (counter = 3, assuming conv with padding = kernel-1)
i_temp = i_load (datamem_off+20+out_channel, datamem_off+17, vec= out_channel) # even row
dict_list.append (i_temp.copy())

i_temp = i_alu ('max', datamem_off+20, datamem_off+20, datamem_off+20+out_channel, vec = out_channel)
dict_list.append (i_temp.copy())

i_temp = i_store (datamem_off+17, datamem_off+20, counter = 3, vec = out_channel) # even row
dict_list.append (i_temp.copy())

## l3_pc - (came from a even col) increment col_curr by 1 and jmp to l1_pc
## l5_pc - (came from odd col, even row)
## increment row_cur, col_cur and proceed to l1_pc
l6_pc = len(dict_list) + 3
i_temp = i_beq (datamem_off+1, datamem_off+3, l6_pc) # check for last column
dict_list.append (i_temp.copy())

# else increment col_curr only
i_temp = i_alu_int ('add', datamem_off+3, datamem_off+3, datamem_off+11) #col_cur++
dict_list.append (i_temp.copy())

i_temp = i_jmp (l1_pc) # restart
dict_list.append (i_temp.copy())

## l6_pc - increment row_cur and reset col_cur
l7_pc = len(dict_list) + 4
i_temp = i_beq (datamem_off+0, datamem_off+2, l7_pc) #check for last row
dict_list.append (i_temp.copy())

i_temp = i_alu_int ('add', datamem_off+2, datamem_off+2, datamem_off+11) #row_cur++
dict_list.append (i_temp.copy())

i_temp = i_set(datamem_off+3, int2bin(0, 16))
dict_list.append (i_temp.copy())

i_temp = i_jmp (l1_pc) # restart
dict_list.append (i_temp.copy())

## l7_pc - program finish
i_temp = i_hlt ()
dict_list.append (i_temp.copy())
filename = temp_dir + '/ima_imem' + str(0) + '.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))



#########################
# Generate ima_imem0.npy for Tile 1 - (LD, MVM, ST) - compute 2 rows of output - MaxPool
# Assumes depth-major data layout (dept -> row -> column)
dict_temp = {}
dict_list = []
out_addr = num_rows * num_in * in_channel
datamem_off = param.num_xbar*param.xbar_size

## Initialization
# set row_max & col_max
row_max = int2bin(num_rows-kernel, 16) # 0 - num_rows-kernel (total - num_rows-kernel+1)
col_max = int2bin(num_in-kernel, 16)
i_temp = i_set (datamem_off, row_max)
dict_list.append (i_temp.copy())
i_temp = i_set (datamem_off+1, col_max)
dict_list.append (i_temp.copy())

# set row_cur & col_cur (current output row or column being computed)
row_cur = int2bin(0, 16)
col_cur = int2bin(0, 16)
i_temp = i_set (datamem_off+2, row_cur)
dict_list.append (i_temp.copy())
i_temp = i_set (datamem_off+3, col_cur)
dict_list.append (i_temp.copy())

edram_rowmax = int2bin(3, 16) # number of rows of input image edram can hold
i_temp = i_set (datamem_off+4, edram_rowmax)
dict_list.append (i_temp.copy())

num_val = int2bin(in_channel * num_in, 16) # number of inputs image pixels per row of edram (num_in * in_channel)
i_temp = i_set (datamem_off+5, num_val)
dict_list.append (i_temp.copy())

num_val = int2bin(in_channel, 16) # number of in_channels
i_temp = i_set (datamem_off+6, num_val)
dict_list.append (i_temp.copy())

## Set the max pool window size and a one for comparison (for odd row/col)
mp = int2bin(2, 16) # max-pool window size
i_temp = i_set (datamem_off+10, mp)
dict_list.append (i_temp.copy())

one = int2bin(1, 16) # one for comparison
i_temp = i_set (datamem_off+11, one)
dict_list.append (i_temp.copy())

## Set the output addr affset
out_addr_off = int2bin(kernel*num_in*num_rows + 4 + out_channel+4, 16)
i_temp = i_set (datamem_off+12, out_addr_off)
dict_list.append (i_temp.copy())

## Set the numout we will compute per row of output map (after max-pool) and out_channel
num_val_out = int2bin(num_out*out_channel, 16)
i_temp = i_set (datamem_off+15, num_val_out)
dict_list.append (i_temp.copy())

num_out_channel = int2bin(out_channel, 16)
i_temp = i_set (datamem_off+16, num_out_channel)
dict_list.append (i_temp.copy())

l1_pc = len(dict_list)
## l1_pc - compute the load addresses for 3 loads (3 rows) based on row_cur & col_cur
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('mod', datamem_off+7, datamem_off+2, datamem_off+4) # first row
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('mul', datamem_off+7, datamem_off+7, datamem_off+5) # (row_curr % 3)*(in_channel*col_max)
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('mul', datamem_off+8, datamem_off+3, datamem_off+6) # col_curr * in_channel
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('add', datamem_off+7, datamem_off+7, datamem_off+8)
dict_list.append (i_temp.copy())

i_temp = i_alu_int ('add', datamem_off+8, datamem_off+7, datamem_off+5) # second row
dict_list.append (i_temp.copy())

i_temp = i_alu_int ('add', datamem_off+9, datamem_off+8, datamem_off+5) # third row
dict_list.append (i_temp.copy())

## load the three rows (each load loads kernel*in_channel values)
vw = kernel*in_channel
for j in range (kernel):
    i_temp = i_load (j*in_channel*kernel, datamem_off+7+j, vw)
    dict_list.append (i_temp.copy())

## copy the values to all 8 xbars (input-sharing)
vw = in_channel * kernel * kernel
for j in range (1,param.num_xbar):
    i_temp = i_copy (j*param.xbar_size, 0, vw)
    dict_list.append (i_temp.copy())

## mvm not using stride support in xbar_inmemstride_val1 = 3
i_temp = i_mvm (8, 0, 0)
dict_list.append (i_temp.copy())

## Check if computing odd col/row
i_temp = i_alu_int ('mod', datamem_off+13, datamem_off+2, datamem_off+10) # check for odd row
dict_list.append (i_temp.copy())

i_temp = i_alu_int ('mod', datamem_off+14, datamem_off+3, datamem_off+10) # check for odd col
dict_list.append (i_temp.copy())

l2_pc = len(dict_list) + param.num_xbar-1 + 3
i_temp = i_beq (datamem_off+14, datamem_off+11, l2_pc)
dict_list.append (i_temp.copy())

## Compute output of conv (shift and add) and relu for even column
vw = out_channel
for j in range (1,param.num_xbar):
    i_temp = i_alu ('sna', datamem_off+20, 0, j*param.xbar_size, j*param.xbar_bits, vec = vw)
    dict_list.append (i_temp.copy())

i_temp = i_alu ('relu', datamem_off+20, datamem_off+20, vec = vw)
dict_list.append (i_temp.copy())

l3_pc = len(dict_list) + param.num_xbar-1 + 15
i_temp = i_jmp (l3_pc)
dict_list.append (i_temp.copy())

## l2_pc - branch target - odd column - conv, relu, half-max
vw = out_channel
for j in range (1,param.num_xbar):
    i_temp = i_alu ('sna', datamem_off+20+out_channel, 0, j*param.xbar_size, j*param.xbar_bits, vec = vw)
    dict_list.append (i_temp.copy())

i_temp = i_alu ('relu', datamem_off+20+out_channel, datamem_off+20+out_channel, vec = vw)
dict_list.append (i_temp.copy())

i_temp = i_alu ('max', datamem_off+20, datamem_off+20, datamem_off+20+out_channel, vec = vw)
dict_list.append (i_temp.copy())

## l4_pc - store the half-max (even row) / full-max value (odd row)
# set the out_addr where output in case of (odd col) gets stored
i_temp = i_alu_int ('div', datamem_off+17, datamem_off+2, datamem_off+10) #row_curr/mp
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('mul', datamem_off+17, datamem_off+17, datamem_off+15) #(row_cur/mp)*(num_out*out_channel)
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('div', datamem_off+18, datamem_off+3, datamem_off+10) #col_cur/mp
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('mul', datamem_off+18, datamem_off+18, datamem_off+16) #(col_cur/mp) * out_channel
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('add', datamem_off+17, datamem_off+17, datamem_off+18) #(row_cur/mp)*(num_out*out_channel) + (col_cur/mp)*(out_channel)
dict_list.append (i_temp.copy())
i_temp = i_alu_int ('add', datamem_off+17, datamem_off+17, datamem_off+12) #out_addr_off + row_cur/mp*num_out + col_cur/mp
dict_list.append (i_temp.copy())

## branch if odd row
l4_pc = len(dict_list) + 3
i_temp = i_beq (datamem_off+13, datamem_off+11, l4_pc)
dict_list.append (i_temp.copy())

i_temp = i_store (datamem_off+17, datamem_off+20, counter = 1, vec = out_channel) # even row
dict_list.append (i_temp.copy())

l5_pc = len(dict_list) + 4
i_temp = i_jmp (l5_pc) # increment col_cur & row_cur
dict_list.append (i_temp.copy())

## l4_pc - odd row - load prev row, do another halt-max (counter = 3, assuming conv with padding = kernel-1)
i_temp = i_load (datamem_off+20+out_channel, datamem_off+17, vec= out_channel) # even row
dict_list.append (i_temp.copy())

i_temp = i_alu ('max', datamem_off+20, datamem_off+20, datamem_off+20+out_channel, vec = out_channel)
dict_list.append (i_temp.copy())

i_temp = i_store (datamem_off+17, datamem_off+20, counter = 3, vec = out_channel) # even row
dict_list.append (i_temp.copy())

## l3_pc - (came from a even col) increment col_curr by 1 and jmp to l1_pc
## l5_pc - (came from odd col, even row)
## increment row_cur, col_cur and proceed to l1_pc
l6_pc = len(dict_list) + 3
i_temp = i_beq (datamem_off+1, datamem_off+3, l6_pc) # check for last column
dict_list.append (i_temp.copy())

# else increment col_curr only
i_temp = i_alu_int ('add', datamem_off+3, datamem_off+3, datamem_off+11) #col_cur++
dict_list.append (i_temp.copy())

i_temp = i_jmp (l1_pc) # restart
dict_list.append (i_temp.copy())

## l6_pc - increment row_cur and reset col_cur
l7_pc = len(dict_list) + 4
i_temp = i_beq (datamem_off+0, datamem_off+2, l7_pc) #check for last row
dict_list.append (i_temp.copy())

i_temp = i_alu_int ('add', datamem_off+2, datamem_off+2, datamem_off+11) #row_cur++
dict_list.append (i_temp.copy())

i_temp = i_set(datamem_off+3, int2bin(0, 16))
dict_list.append (i_temp.copy())

i_temp = i_jmp (l1_pc) # restart
dict_list.append (i_temp.copy())

## l7_pc - program finish
i_temp = i_hlt ()
dict_list.append (i_temp.copy())
filename = temp_dir + '/ima_imem' + str(1) + '.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))

#########################


# Generate all other ima_imem.npy with halts for Tile 1
dict_temp = {}
dict_list = []
i_temp = i_hlt ()
dict_list.append (i_temp.copy())
for i in range (2,param.num_ima):
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

