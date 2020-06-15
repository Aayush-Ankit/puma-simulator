
import sys, os
import numpy as np
import math
sys.path.insert (0, '/home/plinio/puma-simulator/include/')
sys.path.insert (0, '/home/plinio/puma-simulator/src/')
sys.path.insert (0, '/home/plinio/puma-simulator/')
from data_convert import *
from instrn_proto import *
from tile_instrn_proto import *
dict_temp = {}
dict_list = []
i_temp = i_receive(mem_addr=0, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=128, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=256, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=384, vtile_id=9, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=512, vtile_id=11, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=640, vtile_id=13, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=768, vtile_id=15, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=896, vtile_id=17, receive_width=13, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_halt()
dict_list.append(i_temp.copy())
filename = 'vgg16/tile1/tile_imem.npy'
np.save(filename, dict_list)
