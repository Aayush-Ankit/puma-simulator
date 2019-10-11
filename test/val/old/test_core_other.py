## API for testing non-matrix instructions of core - ALU, CP variants
## Set config file to following IMA hyperparameters
#xbar_bits = 2
#num_matrix = 1 # each matrix is 8-fw xbars, 8-bw xbars and 16-delta xbars
#xbar_size = 128
#dac_res = 1
#adc_res = 8
#num_adc = 2 * num_matrix
#num_ALU = 1
#dataMem_size = 4 * (2*xbar_size) # 4 for 4 input spaces within matrix (1 for f/b each, 2 for d)
#instrnMem_size = 512 #in entries

import sys
import os
import numpy as np

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

from src.data_convert import *
import src.ima as ima
from src.instrn_proto import *
import include.configTest as cfg


path = 'coreOther_test/'
inst_file = path + 'imem1.npy'
trace_file = path + 'trace.txt'
dump_file = path + 'memsim.txt'

datamem_off = cfg.datamem_off # each matrix has 6 memory spaces (1 for f/b, 2 for d)
phy2log_ratio = cfg.phy2log_ratio # ratio of physical to logical xbar

## Create memory dump function for an ima
def dump (ima, filename = ''):
    if (filename == ''):
        filename = 'memsim.txt'

    def mem_dump (memfile, name): # for conciseness
        assert (type(memfile) == list), 'memfile should be list'
        fid.write (name + ' contents\n')
        for entry in memfile:
            if (entry != ''):
                temp_val = fixed2float (entry, cfg.int_bits, cfg.frac_bits)
                fid.write(str(temp_val) + '\n')

    fid = open (filename, 'w')
    # dump the datamemory
    mem_dump (ima.dataMem.memfile, 'DataMemory')
    # traverse the matrices in an ima
    mvmu_list = ['f', 'b', 'd']
    for i in range(cfg.num_matrix):
        # traverse mvmus in a matrix
        for mvmu_t in mvmu_list:
            # dump the xbar input memory
            mem_dump (ima.xb_inMem_list[i][mvmu_t].memfile, 'Xbar Input Memory: matrixId: ' + str(i) + 'mvmu_type: '
                    + mvmu_t)
            # dump the xbar output memory
            mem_dump (ima.xb_outMem_list[i][mvmu_t].memfile, 'Xbar Output Memory: matrixId: ' + str(i) + 'mvmu_type: '
                    + mvmu_t)
    fid.close()


## Setup files
phy2log_ratio = cfg.num_bits/cfg.xbar_bits
inst_refresh = 1

## Create core instruction stream for testing
if (inst_refresh):
    num_inst = 0 # track number of instructions generated

    # instructions for IMA1
    dict_list = []
    # Copy data from data memory to xbar_in_memory - Matrix0: f-xbar
    i_temp = i_copy (0, datamem_off+0, cfg.xbar_size)
    dict_list.append (i_temp.copy())

    # Copy data from data memory to xbar_out_memory - Matrix0: b-xbar
    i_temp = i_copy (384, datamem_off+0, cfg.xbar_size)
    dict_list.append (i_temp.copy())

    # Add data copied to above locations and write to data memory
    i_temp = i_alu ('add', datamem_off+128, 0, 384, 0, cfg.xbar_size)
    dict_list.append (i_temp.copy())

    # Add a halt instruction
    i_temp = i_hlt()
    dict_list.append (i_temp.copy())

    print (inst_file + ' generated...')
    np.save (inst_file, dict_list)
    print ('Total no. of instructions: ', len(dict_list))


## Simulate core
ima = ima.ima ()
fid = open(trace_file, "w+")
ima.pipe_init(inst_file, fid)

cycle = 0
while (ima.halt != 1 and cycle < cfg.cycles_max):
    ima.pipe_run (cycle, fid) # fid points to tracefile
    cycle += 1

print (cycle)
fid.close ()
dump (ima, dump_file)


## Testcases for Functionality Debug of different insructions
## compare golden output to ima output
# look memsim.txt to see the data movements from copy instruction




