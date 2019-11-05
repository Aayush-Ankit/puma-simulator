# API for testing MVM inner product operation
import sys
import os
import numpy as np

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

from src.data_convert import *
import src.ima as ima
from src.instrn_proto import *
import include.configTest as cfg


path = 'coreMvm_test/'
wt_path = path
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


### Create a test matrix for MVM functionality check
#xbar_size = cfg.xbar_size
#log_xbar = np.random.randn(xbar_size, xbar_size)
#phy_xbar = [np.random.randn(xbar_size, xbar_size) for i in range(cfg.num_xbar)]
#
## NOTE: weights programmed to xbars are stored in terms of their representative floating values
## for use in np.dot (to store bits representation, use fixed point version of np.dot)
#for i in range (xbar_size):
#    for j in range (xbar_size):
#        temp_val = float2fixed(log_xbar[i][j], cfg.int_bits, cfg.frac_bits)
#        assert (len(temp_val) == 16)
#        for k in range (len(phy_xbar)):
#            if (k==0):
#                val = temp_val[-(k+1)*cfg.xbar_bits:]
#            else:
#                val = temp_val[-(k+1)*cfg.xbar_bits:-(k+1)*cfg.xbar_bits+2]
#            # augment sign extension (used in MSB xbar only)
#            if (k == (len(phy_xbar)-1)):
#                val = (cfg.num_bits - cfg.xbar_bits)*val[0] + val[0:]
#            phy_xbar[k][i][j] = fixed2float(val, cfg.int_bits, cfg.frac_bits)
#
## save log_xbar and phy_xbar to disc
#np.save (wt_path+'log_xbar', log_xbar)
#for i in range (len(phy_xbar)):
#    np.save (wt_path+'phy_xbar'+str(i), phy_xbar[i])


## Setup files
phy2log_ratio = cfg.num_bits/cfg.xbar_bits
inst_refresh = 1

## Create core instruction stream for testing
if (inst_refresh):
    num_inst = 0 # track number of instructions generated

    # instructions for IMA1
    dict_list = []
    # Load data to xbar_in_memory - first Matrix - 'f' MVMU
    i_temp = i_copy (0, datamem_off+0, cfg.xbar_size)
    dict_list.append (i_temp.copy())

    # MVM instruction to populate xbar_out_memory
    i_temp = i_mvm(['100'])
    dict_list.append (i_temp.copy())

    ## MVM_op instruction
    #i_temp = i_mvm(['10'])
    #dict_list.append (i_temp.copy())

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

# program the xbars for matrix0_fw xbar (for functionality check of mvm, using just one matrix is fine)
for i in range (phy2log_ratio):
    wt_temp = np.load(wt_path+'phy_xbar'+str(i)+'.npy')
    ima.matrix_list[0]['f'][i].program(wt_temp)

cycle = 0
while (ima.halt != 1 and cycle < cfg.cycles_max):
    ima.pipe_run (cycle, fid) # fid points to tracefile
    #print (cycle)
    cycle += 1

fid.close ()
dump (ima, dump_file)


## Testcases for Functionality Debug of MVM (1,2,3,4)
# 1. compare golden output to ima output
wt_gold = np.load(wt_path+'log_xbar.npy')
out_gold = np.dot (ima.dataMem.memfile_float, wt_gold)

out_exp = ['']*cfg.xbar_size
for i in range (cfg.xbar_size):
    out_exp[i] = fixed2float(ima.xb_outMem_list[0]['f'].memfile[i], cfg.int_bits, cfg.frac_bits)
out_exp = np.asarray(out_exp)

#print (out_gold)
#print (out_exp)

err = np.tanh(out_gold) - np.tanh(out_exp)
print ("error has mean " + str(np.average(err)) + " and stdev " + \
        str(np.std(err)))

## 2. individual xbar MVM check (no shift-and-add) - PASSED
#wt_gold = np.load (wt_path+'phy_xbar4.npy')
#in_gold = ['']*cfg.xbar_size
#for i in range (cfg.xbar_size):
#    in_gold[i] = fixed2float (15*'0' + ima.dataMem.memfile[i][-1], cfg.int_bits, cfg.frac_bits)
#out_gold = np.dot (in_gold, wt_gold)

## 3. inter-xbar shift-and-add - PASSED
#wt_gold = np.load(wt_path+'log_xbar.npy')
#in_gold = ['']*cfg.xbar_size
#for i in range (cfg.xbar_size):
#    in_gold[i] = fixed2float (15*'0' + ima.dataMem.memfile[i][-1], cfg.int_bits, cfg.frac_bits)
#out_gold = np.dot (in_gold, wt_gold)
#
#out_exp = ['']*cfg.xbar_size
#for i in range (cfg.xbar_size):
#    out_exp[i] = fixed2float(ima.xb_outMem_list[0].memfile[i], cfg.int_bits, cfg.frac_bits)
#out_exp = np.asarray(out_exp)
#

