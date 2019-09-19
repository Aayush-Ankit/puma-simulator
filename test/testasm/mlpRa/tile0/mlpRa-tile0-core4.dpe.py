
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
i_temp = i_hlt()
dict_list.append(i_temp.copy())
filename = 'mlpRa/tile0/core_imem4.npy'
np.save(filename, dict_list)
