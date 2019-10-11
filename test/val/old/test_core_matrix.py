## API for testing matrix instructions of core - MVM-f/b/d, CRS - with one matrix per core only
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


### Create a test matrix for MVM functionality check - positive matrices only
#xbar_size = cfg.xbar_size
## scaling down weight values to ensure that output of MVM doesn't overflow
#log_xbar = 0.1*np.random.rand(xbar_size, xbar_size)
#phy_xbar = [np.random.rand(xbar_size, xbar_size) for i in range(phy2log_ratio)]
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
    # Copy data from data memory to xbar_in_memory - Matrix0: f-xbar
    i_temp = i_copy (0, datamem_off+0, cfg.xbar_size)
    dict_list.append (i_temp.copy())

    # Copy data from data memory to xbar_in_memory - Matrix0: b-xbar
    i_temp = i_copy (256, datamem_off+0, cfg.xbar_size)
    dict_list.append (i_temp.copy())

    # MVM instruction to populate xbar_out_memory - runs inner product on f and b xbar
    i_temp = i_mvm(['110'])
    dict_list.append (i_temp.copy())

    # Copy output of f and b xbars to input memory spaces of d-xbar
    i_temp = i_copy (512, 128, cfg.xbar_size)
    dict_list.append (i_temp.copy())
    i_temp = i_copy (640, 384, cfg.xbar_size)
    dict_list.append (i_temp.copy())

    # MVM instruction to populate d-xbar - runs outer product on d-xbar
    i_temp = i_mvm(['001'])
    dict_list.append (i_temp.copy())

    # CRS instruction to populate populate xbar values in f/b-xbar from d-xbar
    i_temp = i_crs(['1'])
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

# program the xbars for matrix0_fw xbar (for functionality check of mvm, using just one matrix is fine)
for i in range (phy2log_ratio):
    wt_temp = np.load(wt_path+'phy_xbar'+str(i)+'.npy')
    ima.matrix_list[0]['f'][i].program(wt_temp)
    ima.matrix_list[0]['b'][i].program(wt_temp)

cycle = 0
while (ima.halt != 1 and cycle < cfg.cycles_max):
    ima.pipe_run (cycle, fid) # fid points to tracefile
    cycle += 1

print (cycle)
fid.close ()
dump (ima, dump_file)


## Testcases for Functionality Debug of different insructions
## compare golden output to ima output

# 1. MVM instruction - inner-product (fw, bw xbars) -keep upto MVM ('110') instrn
wt_gold = np.load(wt_path+'log_xbar.npy')
out_gold = np.dot (ima.dataMem.memfile_float, wt_gold)

out_expF = ['']*cfg.xbar_size
out_expB = ['']*cfg.xbar_size
for i in range (cfg.xbar_size):
    out_expF[i] = fixed2float(ima.xb_outMem_list[0]['f'].memfile[i], cfg.int_bits, cfg.frac_bits)
    out_expB[i] = fixed2float(ima.xb_outMem_list[0]['b'].memfile[i], cfg.int_bits, cfg.frac_bits)
out_expF = np.asarray(out_expF)
out_expB = np.asarray(out_expB)

errF = abs(np.tanh(out_gold) - np.tanh(out_expF))
errB = abs(np.tanh(out_gold) - np.tanh(out_expB))
print ("fw xbar error has mean " + str(np.average(errF)) + " and stdev " + \
        str(np.std(errF)))
print ("bw xbar error has mean " + str(np.average(errB)) + " and stdev " + \
        str(np.std(errB)))

# 2. MVM instruction - inner-product (f,b xbar), followed by outer-product (d-xbar) - keep upto MVM ('001') instrn
out_goldD = cfg.lr * np.outer (out_expF, out_expB)
out_expD = ima.get_matrix (0, 'd')

errD = abs(out_goldD - out_expD)
print ("delta xbar error has mean " + str(np.average(errD)) + " and stdev " + \
        str(np.std(errD)))

# 3. CRS instruction - read wt slices delta xbars, compose wt, write slices to f/b xbars - keep upto CRS instrn
out_expF = ima.get_matrix (0, 'f')
out_expB = ima.get_matrix (0, 'b')
out_expD = ima.get_matrix (0, 'd')
errFD = abs (out_expF - out_expD)
errBD = abs (out_expB - out_expD)
print ("f-d matrix error has mean " + str(np.average(errFD)) + " and stdev " + \
        str(np.std(errFD)))
print ("b-d matrix error has mean " + str(np.average(errBD)) + " and stdev " + \
        str(np.std(errBD)))




