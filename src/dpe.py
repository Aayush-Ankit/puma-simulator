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
security_dir=os.path.join(root_dir, "Security")

sys.path.insert(1, security_dir)
sys.path.insert(0, include_dir)
sys.path.insert(0, src_dir)
sys.path.insert(0, root_dir)

# Set the instruction & trace paths (create the folder hierarchy)
# Assumption: All instructions for all TILEs and IMAs have already been generated
from data_convert import *
from node_dump import *
from record_xbar import *
from hw_stats import *
import numpy as np

import argparse
import config as cfg
import constants
import ima_modules
import ima
import tile_modules
import tile
import node_modules
import node
import ima_metrics
import tile_metrics
import node_metrics
import dnn_wt_p
from Factory import Factory



compiler_path = os.path.join(root_dir, "test/testasm/")
trace_path = os.path.join(root_dir, "test/traces/")


def count_tiles(net_path):
    t_count = 0
    while os.path.isdir(net_path + "/tile" + str(t_count)):
        t_count += 1
    return t_count


class DPE:

    def run(self, net):
        print(test_dir)
        instrndir = compiler_path + net
        #tracedir = os.path.join(os.path.join(test_dir, 'traces'), net.split('/')[-1])
        tracedir = trace_path + net
        print("Inst directory: ", instrndir)
        print("Trace directory: ", tracedir)

        if cfg.authenticated:
            f = Factory()
            puma_cypher_hash = f.auth(cfg.cypher_hash)

            if not puma_cypher_hash.authenticateModel(instrndir):
                print("Model not authenticated")
                sys.exit(1)
            if not puma_cypher_hash.authenticateInput(instrndir):
                print("Input not authenticated")
                sys.exit(1)

        if cfg.encrypted:
            f = Factory()
            puma_crypto = f.crypto(cfg.cypher_name)
            puma_crypto.decrypt(instrndir)
        assert (os.path.exists(instrndir) ==1), 'Instructions for net missing: generate intuctions (in folder hierarchy) hierarchy'
        '''if not os.path.exists(instrndir):
            os.makedirs(instrndir)
            for i in range (cfg.num_tile):
                temp_tiledir = instrndir + '/tile' + str(i)
                os.makedirs(temp_tiledir)'''

        if not os.path.exists(tracedir):
            os.makedirs(tracedir)

        for i in range(cfg.num_tile):
            temp_tiledir = tracedir + '/tile' + str(i)
            if not os.path.exists(temp_tiledir):
                os.makedirs(temp_tiledir)

        self.instrnpath = instrndir + '/'
        self.tracepath = tracedir + '/'

        # Instantiate the node under test
        # A physical node consists of several logical nodes equal to the actual node size
        node_dut = node.node()

        # Initialize the node with instrn & trace paths
        # instrnpath provides instrns for tile & resident imas
        # tracepath is where all tile & ima traces will be stored
        node_dut.node_init(self.instrnpath, self.tracepath)

        # Read the input data (input.t7) into the input tile's edram
     
        inp_filename = os.path.join(str(self.instrnpath) ,'input.npy')


        inp_tileId = 0
        assert (os.path.exists(inp_filename)
                ), 'Input Error: Provide input before running the DPE'

        assert (os.path.exists(instrndir+'/'+'tile0')
                ), 'Input Error: Provide input before running the DPE'
  
            
        inp = np.load(inp_filename, allow_pickle=True).item()
        print ('length of input data:', len(inp['data']))
        for i in range(len(inp['data'])):
            data = float2fixed(inp['data'][i], cfg.int_bits, cfg.frac_bits)
            node_dut.tile_list[inp_tileId].edram_controller.mem.memfile[i] = data
            node_dut.tile_list[inp_tileId].edram_controller.counter[i] = int(
                inp['counter'][i])
            node_dut.tile_list[inp_tileId].edram_controller.valid[i] = int(
                inp['valid'][i])

        #program the X-bars with weights using the dnn_wt_p.dnn_wt() API

        dnn_wt_p.dnn_wt().prog_dnn_wt(self.instrnpath, node_dut)

        # Run all the tiles
        cycle = 0
        start = time.time()
        while (not node_dut.node_halt and cycle < cfg.cycles_max):
            node_dut.node_run(cycle)
            cycle = cycle + 1

        end = time.time()
        print ('simulation time: ' + str(end-start) + 'secs')

        # For DEBUG only - dump the contents of all tiles
        # NOTE: Output and input tiles are dummy tiles to enable self-contained simulation
        if (cfg.debug):
            node_dump(node_dut, self.tracepath)

        #if (cfg.xbar_record):
        #    record_xbar(node_dut)

        # Dump the contents of output tile (DNN output) to output file (output.txt)
        output_file = self.tracepath + 'output.txt'
        fid = open(output_file, 'w')
        tile_id = cfg.num_tile - 1
        mem_dump(
            fid, node_dut.tile_list[tile_id].edram_controller.mem.memfile, 'EDRAM')
        fid.close()
        print('Output Tile dump finished')

        # Dump the harwdare access traces (For now - later upgrade to actual energy numbers)
        hwtrace_file = self.tracepath + 'harwdare_stats.txt'
        fid = open(hwtrace_file, 'w')
        metric_dict = get_hw_stats(fid, node_dut, cycle)
        fid.close()
        print('Success: Hardware results compiled!!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--net", help="The net name as it is in test/testasm.", default='large')
    parser.add_argument(
            "-t", "--tile", help ="The number of tiles as generated by compiler.", default=-1)
    parser.add_argument(
            '-c',"--cryptography", help="Run an encrypted model")
    parser.add_argument(
            '-a',"--authenticated", help="Run only authenticated models") 
    args = parser.parse_args()
    net = args.net

    cfg.authenticated = True if args.authenticated else False
    
    cfg.encrypted = True if args.cryptography else False 
    cfg.cypher_name = args.cryptography
    cfg.cypher_hash = args.authenticated
    
    
    if cfg.encrypted :
        model_path = os.path.join(compiler_path,net,"crypto") 
    else:
        model_path = os.path.join(compiler_path,net) 

    total_tiles = count_tiles(model_path) - 2
    print(total_tiles)

    if(args.tile != -1):
        total_tiles = int(args.tile)

    cfg.num_tile_compute = total_tiles
    cfg.num_tile = cfg.num_node * cfg.num_tile_compute + 2
    
    #print(cfg.num_tile)
    #print(cfg.encrypted)
    #print(cfg.cypher_name)
   
    print('Input net is {}'.format(net))
    print(compiler_path)
    DPE().run(net)
    
