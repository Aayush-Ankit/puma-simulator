
import sys, os
import numpy as np
import math
sys.path.insert (0, '/home/rodrigo/workspace/dpe-research/dpe_emulate/include/')
sys.path.insert (0, '/home/rodrigo/workspace/dpe-research/dpe_emulate/src/')
from data_convert import *
from instrn_proto import *
from tile_instrn_proto import *
dict_temp = {}
dict_list = []
i_temp = i_receive(mem_addr=0, vtile_id=2, receive_width=10, counter=1, vec=2)
dict_list.append(i_temp.copy())
i_temp = i_halt()
dict_list.append(i_temp.copy())
filename = 'mlpRb/tile1/tile_imem.npy'
np.save(filename, dict_list)
