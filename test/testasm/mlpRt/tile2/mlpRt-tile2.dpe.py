
import sys, os
import numpy as np
import math
sys.path.insert (0, '/home/plinio/dpe_emulate/include/')
sys.path.insert (0, '/home/plinio/dpe_emulate/src/')
from data_convert import *
from instrn_proto import *
from tile_instrn_proto import *
dict_temp = {}
dict_list = []
i_temp = i_receive(mem_addr=20, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=148, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=276, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=404, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=532, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=660, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=788, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=926, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1054, vtile_id=0, receive_width=10, counter=1, vec=1)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1064, vtile_id=2, send_width=10, target_addr=1, vec=1)
dict_list.append(i_temp.copy())
i_temp = i_halt()
dict_list.append(i_temp.copy())
filename = 'mlpRt/tile2/tile_imem.npy'
np.save(filename, dict_list)
