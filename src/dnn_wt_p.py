import os
import sys
import numpy as np

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
include_dir = os.path.join(root_dir, "include")
sys.path.insert(0, include_dir)


import config as cfg

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
