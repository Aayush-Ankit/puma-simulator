
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
i_temp = i_receive(mem_addr=2944, vtile_id=392, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2816, vtile_id=392, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2688, vtile_id=392, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2560, vtile_id=392, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2432, vtile_id=392, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2304, vtile_id=392, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2176, vtile_id=392, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2048, vtile_id=392, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1920, vtile_id=392, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1792, vtile_id=392, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1664, vtile_id=392, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1536, vtile_id=392, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1408, vtile_id=391, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1280, vtile_id=391, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1152, vtile_id=391, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1024, vtile_id=391, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3072, vtile_id=158, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=896, vtile_id=159, send_width=16, target_addr=160, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_halt()
dict_list.append(i_temp.copy())
filename = 'vgg16/tile159/tile_imem.npy'
np.save(filename, dict_list)
