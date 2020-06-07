
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
i_temp = i_receive(mem_addr=256, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=384, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=512, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=640, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=768, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=896, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1024, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1152, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1280, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1408, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1536, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1664, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1792, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1920, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2048, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2176, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2304, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2432, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2560, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2688, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2816, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=2944, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3072, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3200, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3328, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3456, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3584, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3712, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3840, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=3968, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=4096, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=4224, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=4352, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=4480, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=4608, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=4736, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=4864, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=4992, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=5120, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=5248, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=5376, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=5504, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=5632, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=5760, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=5888, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=6016, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=6144, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=6272, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=6400, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=6528, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=6656, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=6784, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=6912, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=7040, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=7168, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=7296, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=7424, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=7552, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=7680, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=7808, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=7936, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=8064, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=8192, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=8320, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=8448, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=8576, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=8704, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=8832, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=8960, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=9088, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=9216, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=9344, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=9472, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=9600, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=9728, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=9856, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=9984, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=10112, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=10240, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=10368, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=10496, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=10624, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=10752, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=10880, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=11008, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=11136, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=11264, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=11392, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=11520, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=11648, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=11776, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=11904, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=12032, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=12160, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=12288, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=12416, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=12544, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=12672, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=12800, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=12928, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=13056, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=13184, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=13312, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=13440, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=13568, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=13696, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=13824, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=13952, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=14080, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=14208, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=14336, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=14464, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=14592, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=14720, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=14848, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=14976, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=15104, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=15232, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=15360, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=15488, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=15616, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=15744, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=15872, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=16000, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=16128, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=16256, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=16384, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=16512, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=16640, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=16768, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=16896, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=17024, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=17152, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=17280, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=17408, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=17536, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=17664, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=17792, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=17920, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=18048, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=18176, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=18304, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=18432, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=18560, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=18688, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=18816, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=18944, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=19072, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=19200, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=19328, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=19456, vtile_id=5, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=19584, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=19712, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=19840, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=19968, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=20096, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=20224, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=20352, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=20480, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=20608, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=20736, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=20864, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=20992, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=21120, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=21248, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=21376, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=21504, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=21632, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=21760, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=21888, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=22016, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=22144, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=22272, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=22400, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=22528, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=22656, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=22784, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=22912, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=23040, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=23168, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=23296, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=23424, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=23552, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=23680, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=23808, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=23936, vtile_id=10, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=24064, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=24192, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=24320, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=24448, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=24576, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=24704, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=24832, vtile_id=7, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=24960, vtile_id=3, receive_width=16, counter=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_halt()
dict_list.append(i_temp.copy())
filename = 'vgg16/tile1/tile_imem.npy'
np.save(filename, dict_list)
