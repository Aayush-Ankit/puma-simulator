## API to dump recorded xbar currents (data-gating analysis)
#import sys
#import os

#root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#include_dir = os.path.join(root_dir, "include")
#sys.path.insert(0, include_dir)
from data_convert import *
import config as cfg
import numpy as np
import matplotlib.pyplot as plt

def record_xbar (node):
    xbar_currents = []
    for i in range (len(node.tile_list)):
        print ('Dumping xbar currents from tile num: ', i)
        for j in range (len(node.tile_list[0].ima_list)):
            for k in range (len(node.tile_list[0].ima_list[0].matrix_list)):
                for l in (node.tile_list[i].ima_list[j].matrix_list[k]['f']):
                # check for empty list
                    if (l.xb_record != []):
                        xbar_currents.append(l.xb_record)
    #print(xbar_currents)
    xbar_currents_arr = np.asarray (xbar_currents)
    print(xbar_currents_arr)

    # Analyze the stats (find curent distribution)
    thresh = np.max(xbar_currents_arr) / 20.0
    #thresh = 0.0
    arr_size = np.size (xbar_currents_arr)
    # nonzero_curr = np.count_nonzero(xbar_currents_arr)
    num_val = np.sum(np.absolute(xbar_currents_arr) > thresh)
    print ('non-zero percentage: ' + str(num_val/float(arr_size)*100)[0:5] + ' %')

    #plt.plot(np.reshape(xbar_currents_arr, arr_size))
    flat_arr = np.reshape(xbar_currents_arr, arr_size)
    weights = np.ones_like(flat_arr)/float(len(flat_arr))
    plt.hist(flat_arr, bins=50, weights=weights)
    plt.title("Xbar current distribution")
    plt.ylabel("Fraction")
    plt.xlabel("Xbar current")
    plt.show()


