
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
i_temp = i_send(mem_addr=0, vtile_id=0, send_width=16, target_addr=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=128, vtile_id=0, send_width=16, target_addr=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=256, vtile_id=0, send_width=16, target_addr=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=384, vtile_id=0, send_width=16, target_addr=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=512, vtile_id=0, send_width=16, target_addr=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=640, vtile_id=0, send_width=16, target_addr=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=768, vtile_id=0, send_width=16, target_addr=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=896, vtile_id=0, send_width=16, target_addr=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1024, vtile_id=0, send_width=10, target_addr=2, vec=1)
dict_list.append(i_temp.copy())
i_temp = i_halt()
dict_list.append(i_temp.copy())
filename = 'mlpRt/tile0/tile_imem.npy'
np.save(filename, dict_list)
