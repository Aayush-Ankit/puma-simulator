
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
i_temp = i_receive(mem_addr=4800, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1920, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=4672, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1792, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=4544, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1664, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=4416, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1536, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=4288, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1408, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=4160, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1280, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=4032, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1152, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3904, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1024, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3776, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=896, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3648, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=768, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3520, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=640, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3392, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=512, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3264, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=384, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3136, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=256, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3008, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=128, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2880, vtile_id=0, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=0, vtile_id=472, send_width=16, target_addr=458, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1920, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1792, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1664, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1536, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1408, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1280, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1152, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1024, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=896, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=768, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=640, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=512, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=384, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=256, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=128, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=0, vtile_id=472, send_width=16, target_addr=460, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1920, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1792, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1664, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1536, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1408, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1280, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1152, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1024, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=896, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=768, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=640, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=512, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=384, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=256, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=128, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=0, vtile_id=472, send_width=16, target_addr=462, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1920, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1792, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1664, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1536, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1408, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1280, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1152, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1024, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=896, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=768, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=640, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=512, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=384, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=256, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=128, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=0, vtile_id=472, send_width=16, target_addr=464, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1920, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1792, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1664, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1536, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1408, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1280, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1152, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1024, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=896, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=768, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=640, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=512, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=384, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=256, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=128, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=0, vtile_id=472, send_width=16, target_addr=466, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1920, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1792, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1664, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1536, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1408, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1280, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1152, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1024, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=896, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=768, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=640, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=512, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=384, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=256, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=128, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=0, vtile_id=472, send_width=16, target_addr=468, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1920, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1792, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1664, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1536, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1408, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1280, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1152, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1024, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=896, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=768, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=640, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=512, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=384, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=256, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=128, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=0, vtile_id=472, send_width=16, target_addr=470, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=2776, vtile_id=472, send_width=13, target_addr=473, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_halt()
dict_list.append(i_temp.copy())
filename = 'vgg16/tile472/tile_imem.npy'
np.save(filename, dict_list)
