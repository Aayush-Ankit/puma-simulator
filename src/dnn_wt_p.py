from functools import partial
from multiprocessing import Pool

#****************************************************************************************
# Designed by - Aayush Ankit
#               School of Elctrical and Computer Engineering
#               Nanoelectronics Research Laboratory
#               Purdue University
#               (aankit at purdue dot edu)
#
# DPEsim - Dot-Product Engine Simulator
#
# Input Tile (tile_id = 0) - has instructions to send input layer data to tiles
#       -> Dump the SEND instructions correponding to input data in this tile
#
# Output Tile (tile_id = num_tile) - has instructions to receive output data from tiles
#       -> Dump the data in EDRAM - that's your DNN output
#
# Other tiles (0 < tile_id < num_tile) - physical tiles used in computations
#****************************************************************************************

import time

import sys
import getopt
import os
import argparse

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(root_dir, "src")
include_dir = os.path.join(root_dir, "include")
test_dir = os.path.join(root_dir, "test")

sys.path.insert(0, include_dir)
sys.path.insert(0, src_dir)
sys.path.insert(0, root_dir)

# Set the instruction & trace paths (create the folder hierarchy)
# Assumption: All instructions for all TILEs and IMAs have already been generated
from node_dump import *
import numpy as np

class dnn_wt:

    def prog_dnn_wt(self, instrnpath, node_dut):  

        ## Program DNN weights on the xbars
        for i in range(1, cfg.num_tile):
            print ('Programming weights of tile no: ', i)
            for j in range(cfg.num_ima):
                print ('Programming ima no: ', j)
                for k in range(cfg.num_matrix):
                    for l in range(cfg.phy2log_ratio):
                        wt_filename = instrnpath + 'weights/tile' + str(i) + '/core'+str(j)+\
                                '/mat'+str(k)+'-phy_xbar'+str(l)+'.npy'
                        if (os.path.exists(wt_filename)):  # check if weights for the xbar exist
                            print ('wtfile exits: ' + 'tile ' + str(i) +
                                   'ima ' + str(j) + 'matrix ' + str(k) + 'xbar' + str(l))
                            wt_temp = np.load(wt_filename)
                            node_dut.tile_list[i].ima_list[j].matrix_list[k]['f'][l].program(wt_temp)
                            node_dut.tile_list[i].ima_list[j].matrix_list[k]['b'][l].program(wt_temp)


