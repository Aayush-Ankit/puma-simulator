##  TESTING BACKPROP ON 3-LAYERED MLP
import sys
import os
import numpy as np

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

from src.data_convert import *
from src.instrn_proto import *
from src.tile_instrn_proto import *
import include.config as cfg

path = 'testasm/mlp_train_2layer/' #path for weights, instruction and input for tile0
net = 'mlp_train_2layer'
wt_path  =path + 'weights/'
datamem_off = cfg.datamem_off # each matrix has 6 memory spaces (1 for f/b, 2 for d)
phy2log_ratio = cfg.phy2log_ratio # ratio of physical to logical xbar
inst_refresh = 1


## CREATE MEMRISTOR PROGRAMMING MATRICES
# NOTE: weights programmed to xbars are stored in terms of their representative floating values
xbar_size = cfg.xbar_size
for m in range(cfg.num_matrix):
    ## Create xbar weight files for programming for each matrix
    # scaling down weight values to ensure that output of MVM doesn't overflow
    log_xbar = 0.1*np.random.rand(xbar_size, xbar_size)
    phy_xbar = [np.random.rand(xbar_size, xbar_size) for i in range(phy2log_ratio)]
    xbar_size = cfg.xbar_size
    for i in range (xbar_size):
        for j in range (xbar_size):
            temp_val = float2fixed(log_xbar[i][j], cfg.int_bits, cfg.frac_bits)
            assert (len(temp_val) == 16)
            for k in range (len(phy_xbar)):
                if (k==0):
                    val = temp_val[-(k+1)*cfg.xbar_bits:]
                else:
                    val = temp_val[-(k+1)*cfg.xbar_bits:-(k+1)*cfg.xbar_bits+2]
                # augment sign extension (used in MSB xbar only)
                if (k == (len(phy_xbar)-1)):
                    val = (cfg.num_bits - cfg.xbar_bits)*val[0] + val[0:]
                phy_xbar[k][i][j] = fixed2float(val, cfg.int_bits, cfg.frac_bits)

    # save log_xbar and phy_xbar to disc
    np.save (wt_path+'tile'+str(1)+'/core'+str(0)+'/mat'+str(m)+'-log_xbar', log_xbar)
    for i in range (len(phy_xbar)):
        np.save (wt_path+'tile'+str(1)+'/core'+str(0)+'/mat'+str(m)+'-phy_xbar'+str(i), phy_xbar[i])


## CREATE INSTRUCTIONS FOR PROGRAMMMING PUMA
# Create Tile0 instructions
dict_list = []
# Send input layer data to Tile1
i_temp = i_send(mem_addr=0, vtile_id=0, send_width=16, target_addr=1, vec=8)
dict_list.append(i_temp.copy())

# Add a halt instruction
i_temp = i_halt()
dict_list.append (i_temp.copy())

filename = path+'/tile0/tile_imem.npy'
np.save(filename, dict_list)
print ('Total no. of instructions: ', len(dict_list))

# Create Tile0-IMA0 instructions
dict_list = []
# Add a halt instruction
i_temp = i_hlt()
dict_list.append (i_temp.copy())

filename = path+'/tile0/core_imem0.npy'
np.save(filename, dict_list)
print ('Total no. of instructions: ', len(dict_list))

# Create Tile1 instructions
dict_list = []
# Receive input layer data from Tile0
i_temp = i_receive(mem_addr=0, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())

# Add a halt instruction
i_temp = i_halt()
dict_list.append (i_temp.copy())

filename = path+'/tile1/tile_imem.npy'
np.save(filename, dict_list)
print ('Total no. of instructions: ', len(dict_list))

# Create Tile1-IMA0 instructions
# instructions for IMA1
dict_list = []
# Set load address (load indirect: tileMemory 0-127 holds input data)
i_temp = i_set(d1=datamem_off+0, imm=0, vec=1)
dict_list.append(i_temp.copy())

# Set store address (store indirect: tileMemory 128-255 holds input data)
i_temp = i_set(d1=datamem_off+1, imm=cfg.xbar_size, vec=1)
dict_list.append(i_temp.copy())

# Load data from tile memory to mat0-f-inMem (Matrix0: f-xbar: xbar_inMem)
i_temp = i_load (0, datamem_off+0, load_width=16, vec=cfg.xbar_size/16)
dict_list.append (i_temp.copy())

# MVM instruction to foward pass for layer 0 (MVMU0)
i_temp = i_mvm(['100', '000'])
dict_list.append (i_temp.copy())

# Copy output of layer0-fw pass to enable layer1-fw-pass (from mat0-f-outMem to mat1-f-inMem)
i_temp = i_copy (6*cfg.xbar_size, cfg.xbar_size, cfg.xbar_size)
dict_list.append (i_temp.copy())

# MVM instruction to foward pass for layer 1 (MVMU1)
i_temp = i_mvm(['000', '100'])
dict_list.append (i_temp.copy())

# Copy output of layer1-fw-pass to enable layer1-bw-pass (from mat1-f-outMem to mat1-b-inMem)
i_temp = i_copy (8*cfg.xbar_size, 7*cfg.xbar_size, cfg.xbar_size)
dict_list.append (i_temp.copy())

# Copy output of layer1-fw-pass to enable layer1-acc (from mat1-f-outMem to mat1-d-outMem)
i_temp = i_copy (11*cfg.xbar_size, 7*cfg.xbar_size, cfg.xbar_size)
dict_list.append (i_temp.copy())

# Copy output of layer0-fw pass to enable layer2-acc (from mat0-f-outMem to mat1-d-inMem)
i_temp = i_copy (10*cfg.xbar_size, cfg.xbar_size, cfg.xbar_size)
dict_list.append (i_temp.copy())

# MVM instruction to backward pass for layer 1 and acc for layer 1 (MVMU1)
i_temp = i_mvm(['000', '011'])
dict_list.append (i_temp.copy())

# Copy output of layer1-bw-pass to enable layer0-acc (from mat1-b-outMem to mat0-d-outMem)
i_temp = i_copy (5*cfg.xbar_size, 9*cfg.xbar_size, cfg.xbar_size)
dict_list.append (i_temp.copy())

# Copy output of layer0-fw pass to enable layer2-acc (from mat0-f-outMem to mat0-d-inMem)
i_temp = i_copy (4*cfg.xbar_size, cfg.xbar_size, cfg.xbar_size)
dict_list.append (i_temp.copy())

# MVM instruction to acc for layer 0 (MVMU0)
i_temp = i_mvm(['001', '000'])
dict_list.append (i_temp.copy())

## CRS instruction to populate populate xbar values in f/b-xbar from d-xbar for MVMU 0&1
#i_temp = i_crs(['1', '1'])
#dict_list.append (i_temp.copy())

## Store output of layer 1 to tile memory
#i_temp = i_store(d1=datamem_off+1, r1=7*cfg.xbar_size, counter=1, store_width=16, vec=cfg.xbar_size/16)
#dict_list.append(i_temp.copy())

# Add a halt instruction
i_temp = i_hlt()
dict_list.append (i_temp.copy())

filename = path+'/tile1/core_imem0.npy'
np.save(filename, dict_list)
print ('Total no. of instructions: ', len(dict_list))


## VALIDATE WITH SOFTWARE OUTPUT (compare new weight after back-prop)


