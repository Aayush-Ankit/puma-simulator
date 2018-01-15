# Generates instructions that are used by ima
# add the folder location for include files
import sys
sys.path.insert (0, '/home/aa/dpe_emulate/include')

import numpy as np
import constants as param
from tile_instrn_proto import *

instrnpath = '/home/aa/dpe_emulate/test/testasm/LSTM2_new/tile2/'
num_inst = 0 # global variable keeps track of num instructions generated

## Instruction for Tile
dict_list = []
# 4 receive instructions (i_t)
i_temp = i_receive (0, 0, 3)
dict_list.append (i_temp.copy())

i_temp = i_receive (1, 1, 3)
dict_list.append (i_temp.copy())

i_temp = i_receive (2, 2, 3)
dict_list.append (i_temp.copy())

i_temp = i_receive (3, 3, 3)
dict_list.append (i_temp.copy())

# 3 receive instructions (h_t)
i_temp = i_receive (4, 4, 3)
dict_list.append (i_temp.copy())

i_temp = i_receive (5, 5, 3)
dict_list.append (i_temp.copy())

i_temp = i_receive (6, 6, 3)
dict_list.append (i_temp.copy())

# 3 receive instructions (c_t)
i_temp = i_receive (7, 7, 1)
dict_list.append (i_temp.copy())

i_temp = i_receive (8, 8, 1)
dict_list.append (i_temp.copy())

i_temp = i_receive (9, 9, 1)
dict_list.append (i_temp.copy())

# Add a tile_compute instruction
i_temp = i_compute ('1'*param.num_ima)
dict_list.append (i_temp.copy())

# Add 3 sends (ct) - tile 0 sends to tile1
i_temp = i_send (22, 7, '011')
dict_list.append (i_temp.copy())

i_temp = i_send (23, 8, '011')
dict_list.append (i_temp.copy())

i_temp = i_send (24, 9, '011')
dict_list.append (i_temp.copy())

# Add 3 sends (ht) - tile 0 sends to til1
i_temp = i_send (25, 4, '011')
dict_list.append (i_temp.copy())

i_temp = i_send (26, 5, '011')
dict_list.append (i_temp.copy())

i_temp = i_send (27, 6, '011')
dict_list.append (i_temp.copy())

# Add a halt instruction
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = instrnpath + 'tile_imem.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))
