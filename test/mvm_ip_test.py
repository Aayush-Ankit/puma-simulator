# API for testing MVM inner product operation
import sys
import os
import numpy as np

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

from src.data_convert import *
import src.ima as ima
from src.instrn_proto import *
import include.config as cfg

#change the core and mvmu id'd here:
# tile_ID = 2
# core_ID = 1
# matrix_ID = 0

for tile_ID in range(2, cfg.num_tile):
    for core_ID in range(cfg.num_ima):
        for matrix_ID in range(cfg.num_matrix):

            path = 'testasm/mlp/'
            wt_path = path +'weights/tile'+ str(tile_ID)+ '/core'+ str(core_ID)+ '/' 
            inst_file = path + 'tile'+ str(tile_ID)+ '/core_imem'+ str(core_ID)+ '.npy'
            trace_path = 'traces/mlp/'
            trace_file = trace_path + 'tile'+ str(tile_ID)+ '/ima_trace'+ str(core_ID)+ '.txt'
            dump_file = trace_path + 'tile'+ str(tile_ID)+ '/memsim.txt'

            datamem_off = cfg.datamem_off # each matrix has 6 memory spaces (1 for f/b, 2 for d)
            phy2log_ratio = cfg.phy2log_ratio # ratio of physical to logical xbar
            
            if (os.path.exists(wt_path)):  # check if weights for the xbar exist
                # print ('wtfile exits: ' + 'tile' + str(tile_ID) +' core ' + str(core_ID) + 'matrix ' + str(matrix_ID))
            
                xbar_input = ['']*cfg.xbar_size
                xbar_output = ['']*cfg.xbar_size
                with open(dump_file, 'r') as file:
                    lines=file.readlines()

                for i in range (len(lines)):
                    if(lines[i] == 'Xbar Input Memory: imaId:'+ str(core_ID)+ ' matrixId:'+ str(matrix_ID)+ ' mvmu_type:f contents\n'):
                        ip_start=i+1
                    if(lines[i] == 'Xbar Output Memory: imaId:'+ str(core_ID)+ ' matrixId:'+ str(matrix_ID)+ ' mvmu_type:f contents\n'):
                        op_start=i+1
                        ip_end=i-1
                    if(lines[i] == 'Xbar Input Memory: imaId:'+ str(core_ID)+ ' matrixId:'+ str(matrix_ID)+ ' mvmu_type:b contents\n'):
                        op_end=i-1

                # print(ip_start)
                # print(ip_end)
                # print(op_start)
                # print(op_end)
                # print('Length of input=',ip_end-ip_start+1 )
                # print('Length of output=',op_end-op_start+1 )

                for j in range (ip_end-ip_start+1):
                    xbar_input[j] = float(lines[ip_start+j])
                for j in range (op_end-op_start+1):
                    xbar_output[j] = float(lines[op_start+j])

                # print(xbar_input)
                # print(xbar_output)

                ## Testcases for Functionality Debug of MVM (1,2,3,4)
                ## 1. compare golden output to ima output
                wt_gold = np.load(wt_path+'log_xbar0.npy')
                # print(wt_gold)
                # out_gold = np.dot (ima.dataMem.memfile_float, wt_gold)
                if(ip_end-ip_start+1 == 128):

                    out_gold = np.dot (np.asarray(xbar_input), wt_gold)
                    out_exp = np.asarray(xbar_output)

                    # print (out_gold)
                    # print (out_exp)

                    err = np.tanh(out_gold) - np.tanh(out_exp)
                    print ("error for tile"+ str(tile_ID) +" core" + str(core_ID) + " matrix" + str(matrix_ID)+ " has mean= " + str(np.average(err)) + " and stdev= " + \
                            str(np.std(err)))
                            
                else:
                    print("No or less than length 128 input available for tile"+ str(tile_ID) +" core" + str(core_ID) + " matrix" + str(matrix_ID)+".")
