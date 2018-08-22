# Generates instructions that are used by ima
# add the folder location for include files
import sys
sys.path.insert (0, '/home/michael/hp_dpe/dpe_emulate-br/include')

import numpy as np
import constants as param
from tile_instrn_proto import *

instrnpath = '/home/aa/dpe_emulate/test/testasm/LSTM2_new/tile3/'
num_inst = 0 # global variable keeps track of num instructions generated

## Instruction for Tile
dict_list = []
'''# Add 4 sends (inp1) - tile 0 sends to tile1
i_temp = i_send (0, 0, '001')
dict_list.append (i_temp.copy())

i_temp = i_send (1, 1, '001')
dict_list.append (i_temp.copy())

i_temp = i_send (2, 2, '001')
dict_list.append (i_temp.copy())

i_temp = i_send (3, 3, '001')
dict_list.append (i_temp.copy())

# Add 3 sends (h0) - tile 0 sends to tile1
i_temp = i_send (4, 4, '001')
dict_list.append (i_temp.copy())

i_temp = i_send (5, 5, '001')
dict_list.append (i_temp.copy())

i_temp = i_send (6, 6, '001')
dict_list.append (i_temp.copy())

# Add 3 sends (c0) - tile 0 sends to tile1
i_temp = i_send (7, 7, '001')
dict_list.append (i_temp.copy())

i_temp = i_send (8, 8, '001')
dict_list.append (i_temp.copy())

i_temp = i_send (9, 9, '001')
dict_list.append (i_temp.copy())

# Add 4 sends (inp2) - tile 0 sends to tile2
i_temp = i_send (10, 0, '010')
dict_list.append (i_temp.copy())

i_temp = i_send (11, 1, '010')
dict_list.append (i_temp.copy())

i_temp = i_send (12, 2, '010')
dict_list.append (i_temp.copy())

i_temp = i_send (13, 3, '010')
dict_list.append (i_temp.copy())'''

# Add 3 receives (h2) - Tile 3 receievs from Tile 2
i_temp = i_receive (0, 7, 1)
dict_list.append (i_temp.copy())

i_temp = i_receive (1, 8, 1)
dict_list.append (i_temp.copy())

i_temp = i_receive (2, 9, 1)
dict_list.append (i_temp.copy())

# Add 3 receives (c2) - Tile 3 receievs from Tile 2
i_temp = i_receive (3, 4, 1)
dict_list.append (i_temp.copy())

i_temp = i_receive (4, 5, 1)
dict_list.append (i_temp.copy())

i_temp = i_receive (5, 6, 1)
dict_list.append (i_temp.copy())

# Add a halt instruction
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = instrnpath + 'tile_imem.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))
