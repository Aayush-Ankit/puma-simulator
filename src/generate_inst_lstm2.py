# Generates instructions that are used by ima
# add the folder location for include files
import sys
sys.path.insert (0, '/home/aa/dpe_emulate/include')

import numpy as np
import constants as param
from instrn_proto import *

instrnpath = '/home/aa/dpe_emulate/test/testasm/LSTM2_new/tile3/'
num_inst = 0 # global variable keeps track of num instructions generated

# Generate actual instructions
datamem_off = param.num_xbar * param.xbar_size # offset tells where datamem starts

### Instruction for IMA1
dict_list = []
# Load Input data - 4*3 Load data to xb_inMem0/1/2
i_temp = i_load (0, 0)
dict_list.append (i_temp.copy())
i_temp = i_load (1, 1)
dict_list.append (i_temp.copy())
i_temp = i_load (2, 2)
dict_list.append (i_temp.copy())
i_temp = i_load (3, 3)
dict_list.append (i_temp.copy())
i_temp = i_load (4, 0)
dict_list.append (i_temp.copy())
i_temp = i_load (5, 1)
dict_list.append (i_temp.copy())
i_temp = i_load (6, 2)
dict_list.append (i_temp.copy())
i_temp = i_load (7, 3)
dict_list.append (i_temp.copy())
i_temp = i_load (8, 0)
dict_list.append (i_temp.copy())
i_temp = i_load (9, 1)
dict_list.append (i_temp.copy())
i_temp = i_load (10, 2)
dict_list.append (i_temp.copy())
i_temp = i_load (11, 3)
dict_list.append (i_temp.copy())

# Load previous cell state into datamemory
i_temp = i_load (datamem_off + 0, 7)
dict_list.append (i_temp.copy())
i_temp = i_load (datamem_off + 1, 8)
dict_list.append (i_temp.copy())
i_temp = i_load (datamem_off + 2, 9)
dict_list.append (i_temp.copy())

# mvm instrn - 3 xbars (3 for i2h)
i_temp = i_mvm (3)
dict_list.append (i_temp.copy())

# 12 Load h2h computed by other ima (datamem_off 3-14)
i_temp = i_load (datamem_off + 3,  10)
dict_list.append (i_temp.copy())
i_temp = i_load (datamem_off + 4,  11)
dict_list.append (i_temp.copy())
i_temp = i_load (datamem_off + 5,  12)
dict_list.append (i_temp.copy())
i_temp = i_load (datamem_off + 6,  13)
dict_list.append (i_temp.copy())
i_temp = i_load (datamem_off + 7,  14)
dict_list.append (i_temp.copy())
i_temp = i_load (datamem_off + 8,  15)
dict_list.append (i_temp.copy())
i_temp = i_load (datamem_off + 9,  16)
dict_list.append (i_temp.copy())
i_temp = i_load (datamem_off + 10, 17)
dict_list.append (i_temp.copy())
i_temp = i_load (datamem_off + 11, 18)
dict_list.append (i_temp.copy())
i_temp = i_load (datamem_off + 12, 19)
dict_list.append (i_temp.copy())
i_temp = i_load (datamem_off + 13, 20)
dict_list.append (i_temp.copy())
i_temp = i_load (datamem_off + 14, 21)
dict_list.append (i_temp.copy())

# 12 ALU instructions for Vector add
i_temp = i_alu ('add', datamem_off + 3,   0,   datamem_off + 3)
dict_list.append (i_temp.copy())
i_temp = i_alu ('add', datamem_off + 4,   1,   datamem_off + 4)
dict_list.append (i_temp.copy())
i_temp = i_alu ('add', datamem_off + 5,   2,   datamem_off + 5)
dict_list.append (i_temp.copy())
i_temp = i_alu ('add', datamem_off + 6,   3,   datamem_off + 6)
dict_list.append (i_temp.copy())
i_temp = i_alu ('add', datamem_off + 7,   4,   datamem_off + 7)
dict_list.append (i_temp.copy())
i_temp = i_alu ('add', datamem_off + 8,   5,   datamem_off + 8)
dict_list.append (i_temp.copy())
i_temp = i_alu ('add', datamem_off + 9,   6,   datamem_off + 9)
dict_list.append (i_temp.copy())
i_temp = i_alu ('add', datamem_off + 10,  7,   datamem_off + 10)
dict_list.append (i_temp.copy())
i_temp = i_alu ('add', datamem_off + 11,  8,   datamem_off + 11)
dict_list.append (i_temp.copy())
i_temp = i_alu ('add', datamem_off + 12,  9,   datamem_off + 12)
dict_list.append (i_temp.copy())
i_temp = i_alu ('add', datamem_off + 13,  10,  datamem_off + 13)
dict_list.append (i_temp.copy())
i_temp = i_alu ('add', datamem_off + 14,  11,  datamem_off + 14)
dict_list.append (i_temp.copy())

# 12 ALU instructions for Vector non-linearity
# input gate
i_temp = i_alu ('sig', datamem_off + 3,  datamem_off + 3,  '', '')
dict_list.append (i_temp.copy())
i_temp = i_alu ('sig', datamem_off + 4,  datamem_off + 4,  '', '')
dict_list.append (i_temp.copy())
i_temp = i_alu ('sig', datamem_off + 5,  datamem_off + 5,  '', '')
dict_list.append (i_temp.copy())
# forget gate
i_temp = i_alu ('sig', datamem_off + 6,  datamem_off + 6,  '', '')
dict_list.append (i_temp.copy())
i_temp = i_alu ('sig', datamem_off + 7,  datamem_off + 7,  '', '')
dict_list.append (i_temp.copy())
i_temp = i_alu ('sig', datamem_off + 8,  datamem_off + 8,  '', '')
dict_list.append (i_temp.copy())
# output gate
i_temp = i_alu ('sig', datamem_off + 9,  datamem_off + 9,  '', '')
dict_list.append (i_temp.copy())
i_temp = i_alu ('sig', datamem_off + 10, datamem_off + 10, '', '')
dict_list.append (i_temp.copy())
i_temp = i_alu ('sig', datamem_off + 11, datamem_off + 11, '', '')
dict_list.append (i_temp.copy())
# c_int
i_temp = i_alu ('sig', datamem_off + 12, datamem_off + 12, '', '')
dict_list.append (i_temp.copy())
i_temp = i_alu ('sig', datamem_off + 13, datamem_off + 13, '', '')
dict_list.append (i_temp.copy())
i_temp = i_alu ('sig', datamem_off + 14, datamem_off + 14, '', '')
dict_list.append (i_temp.copy())

# 3 ALU instructions for ALU multiply - c_prev .* forget
i_temp = i_alu ('mul', datamem_off + 0, datamem_off + 0, datamem_off + 6)
dict_list.append (i_temp.copy())
i_temp = i_alu ('mul', datamem_off + 1, datamem_off + 1, datamem_off + 7)
dict_list.append (i_temp.copy())
i_temp = i_alu ('mul', datamem_off + 2, datamem_off + 2, datamem_off + 8)
dict_list.append (i_temp.copy())

# 3 ALU instructions for ALU multiply - input .* c_int
i_temp = i_alu ('mul', datamem_off + 3, datamem_off + 3, datamem_off + 12)
dict_list.append (i_temp.copy())
i_temp = i_alu ('mul', datamem_off + 4, datamem_off + 4, datamem_off + 13)
dict_list.append (i_temp.copy())
i_temp = i_alu ('mul', datamem_off + 5, datamem_off + 5, datamem_off + 14)
dict_list.append (i_temp.copy())

# ALU instructions for ALU add - vector ADD - c_next (one of the outputs)
i_temp = i_alu ('add', datamem_off + 0, datamem_off + 0, datamem_off + 3)
dict_list.append (i_temp.copy())
i_temp = i_alu ('add', datamem_off + 1, datamem_off + 1, datamem_off + 4)
dict_list.append (i_temp.copy())
i_temp = i_alu ('add', datamem_off + 2, datamem_off + 2, datamem_off + 5)
dict_list.append (i_temp.copy())

# ALU instructins for non-linearity
i_temp = i_alu ('sig', datamem_off + 3, datamem_off + 0, '', '')
dict_list.append (i_temp.copy())
i_temp = i_alu ('sig', datamem_off + 4, datamem_off + 1, '', '')
dict_list.append (i_temp.copy())
i_temp = i_alu ('sig', datamem_off + 5, datamem_off + 2, '', '')
dict_list.append (i_temp.copy())

# 3 ALU instructions for ALU multiply - h_t
i_temp = i_alu ('mul', datamem_off + 3, datamem_off + 3, datamem_off + 9)
dict_list.append (i_temp.copy())
i_temp = i_alu ('mul', datamem_off + 4, datamem_off + 4, datamem_off + 10)
dict_list.append (i_temp.copy())
i_temp = i_alu ('mul', datamem_off + 5, datamem_off + 5, datamem_off + 11)
dict_list.append (i_temp.copy())

# 6 Stores - Vector store to store back the output to EDRAM
i_temp = i_store (datamem_off + 0, 22)
dict_list.append (i_temp.copy())
i_temp = i_store (datamem_off + 1, 23)
dict_list.append (i_temp.copy())
i_temp = i_store (datamem_off + 2, 24)
dict_list.append (i_temp.copy())
i_temp = i_store (datamem_off + 3, 25)
dict_list.append (i_temp.copy())
i_temp = i_store (datamem_off + 4, 26)
dict_list.append (i_temp.copy())
i_temp = i_store (datamem_off + 5, 27)
dict_list.append (i_temp.copy())

# Add a halt instruction
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = instrnpath + 'ima_imem0.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))


### Instruction for IMA2
dict_list = []
# Load Hidden State Data - 3*3 Load data to xb_inMem1 - for Hidden state data
i_temp = i_load (0,  4)
dict_list.append (i_temp.copy())
i_temp = i_load (1,  5)
dict_list.append (i_temp.copy())
i_temp = i_load (2,  6)
dict_list.append (i_temp.copy())
i_temp = i_load (4,  4)
dict_list.append (i_temp.copy())
i_temp = i_load (5,  5)
dict_list.append (i_temp.copy())
i_temp = i_load (6,  6)
dict_list.append (i_temp.copy())
i_temp = i_load (8,  4)
dict_list.append (i_temp.copy())
i_temp = i_load (9,  5)
dict_list.append (i_temp.copy())
i_temp = i_load (10, 6)
dict_list.append (i_temp.copy())

# mvm instrn - 6 xbars (3 for i2h, 3 for h2h)
i_temp = i_mvm (3)
dict_list.append (i_temp.copy())

# Store values to be transfered to IMA1
i_temp = i_store (0,  10)
dict_list.append (i_temp.copy())
i_temp = i_store (1,  11)
dict_list.append (i_temp.copy())
i_temp = i_store (2,  12)
dict_list.append (i_temp.copy())
i_temp = i_store (3,  13)
dict_list.append (i_temp.copy())
i_temp = i_store (4,  14)
dict_list.append (i_temp.copy())
i_temp = i_store (5,  15)
dict_list.append (i_temp.copy())
i_temp = i_store (6,  16)
dict_list.append (i_temp.copy())
i_temp = i_store (7,  17)
dict_list.append (i_temp.copy())
i_temp = i_store (8,  18)
dict_list.append (i_temp.copy())
i_temp = i_store (9,  19)
dict_list.append (i_temp.copy())
i_temp = i_store (10, 20)
dict_list.append (i_temp.copy())
i_temp = i_store (11, 21)
dict_list.append (i_temp.copy())

# Add a halt instruction
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = instrnpath + 'ima_imem1.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))

