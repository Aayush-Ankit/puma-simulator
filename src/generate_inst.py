# Generates instructions that are used by ima
# add the folder location for include files
import sys
sys.path.insert (0, '/home/michael/hp_dpe/dpe_emulate-br/include')

import numpy as np
import constants as param
from instrn_proto import *

instrnpath = '/home/ankitaay/dpe/test/testasm/ima_sync/'
num_inst = 0 # global variable keeps track of num instructions generated

# Generate actual instructions
datamem_off = param.num_xbar * param.xbar_size # offset tells where datamem starts

### Instruction for IMA1
dict_list = []
# Load data to data memory
i_temp = i_load (datamem_off + 0, 1)
dict_list.append (i_temp.copy())

# ALUi instructions for add
i_temp = i_alu ('add', datamem_off + 1, datamem_off + 0, '', '0011'*2)
dict_list.append (i_temp.copy())

# Store instruction
i_temp = i_store (datamem_off + 1, 2)
dict_list.append (i_temp.copy())

# Add a halt instruction
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = instrnpath + 'imem1.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))

### Instruction for IMA2
dict_list = []
# Load data to data memory
i_temp = i_load (datamem_off + 0, 0)
dict_list.append (i_temp.copy())

# ALUi instructions for add
i_temp = i_alu ('add', datamem_off + 1, datamem_off + 0, '', '0011'*2)
dict_list.append (i_temp.copy())

# Store instruction
i_temp = i_store (datamem_off + 1, 1)
dict_list.append (i_temp.copy())

# Add a halt instruction
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = instrnpath + 'imem2.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))


