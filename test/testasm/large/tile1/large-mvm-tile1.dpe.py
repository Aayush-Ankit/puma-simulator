
import sys, os
import numpy as np
import math
sys.path.insert (0, '/home/tensor/aa_dpe_emulate/include/')
sys.path.insert (0, '/home/tensor/aa_dpe_emulate/src/')
from data_convert import *
from instrn_proto import *
from tile_instrn_proto import *
dict_temp = {}
dict_list = []
i_temp = i_receive(mem_addr=128, vtile_id=2, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=256, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=384, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=0, vtile_id=2, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_halt()
dict_list.append(i_temp.copy())
filename = 'large/tile1/tile_imem.npy'
np.save(filename, dict_list)
