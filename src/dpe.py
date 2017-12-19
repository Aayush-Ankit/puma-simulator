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


class DPE:

    def __init__(self, net):
        instrndir = os.path.join(os.path.join(test_dir, 'testasm'), net)
        tracedir = os.path.join(os.path.join(test_dir, 'traces'), net)

        assert (os.path.exists(instrndir) ==
                1), 'Instructions for net missing: generate intuctions (in folder hierarchy) hierarchy'
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

    def run(self):
        # Instantiate the node under test
        # A physical node consists of several logical nodes equal to the actual node size
        node_dut = node.node()

        # Initialize the node with instrn & trace paths
        # instrnpath provides instrns for tile & resident imas
        # tracepath is where all tile & ima traces will be stored
        node_dut.node_init(self.instrnpath, self.tracepath)

        # Read the input data (input.t7) into the input tile's edram(controller)
        inp_filename = self.instrnpath + 'input.npy'
        inp_tileId = 0
        assert (os.path.exists(inp_filename)
                ), 'Input Error: Provide inputbefore running the DPE'
        inp = np.load(inp_filename).item()
        print (len(inp['data']))
        for i in range(len(inp['data'])):
            data = float2fixed(inp['data'][i], cfg.int_bits, cfg.frac_bits)
            node_dut.tile_list[inp_tileId].edram_controller.mem.memfile[i] = data
            node_dut.tile_list[inp_tileId].edram_controller.counter[i] = int(
                inp['counter'][i])
            node_dut.tile_list[inp_tileId].edram_controller.valid[i] = int(
                inp['valid'][i])

        # Program DNN weights on the xbars
        # torch table in file - (tracepath/tile<>/weights/ima<>_xbar<>.t7)
        #for i in range(1, cfg.num_tile - 1):
        #    print ('Programming tile no: ', i)
        #    for j in range(cfg.num_ima):
        #        print ('Programming ima no: ', j)
        #        for k in range(cfg.num_xbar):
        #            wt_filename = self.instrnpath + 'tile' + str(i) + '/weights/' + \
        #                'ima' + str(j) + '_xbar' + str(k) + '.npy'
        #            #'ima' + str(j) + '_xbar' + str(k) + '.t7'
        #            if (os.path.exists(wt_filename)):  # check if weights for the xbar exist
        #                print ('wtfile exits: ' + 'tile ' + str(i) +
        #                       'ima ' + str(j) + 'xbar ' + str(k))
        #                #wt_temp = tf.load (wt_filename)
        #                wt_temp = np.load(wt_filename)
        #                node_dut.tile_list[i].ima_list[j].xbar_list[k].program(
        #                    wt_temp)

        #raw_input ('Press Enter')

        # Run all the tiles
        cycle = 0
        start = time.time()
        while (not node_dut.node_halt and cycle < cfg.cycles_max):
            ## run tiles in parallel
            #tile_func = partial(node_dut.node_tile_run, cycle)
            #print ('tile proc running')
            #iterable = range(cfg.num_tile)
            #pool = Pool()
            #pool.map (tile_func, iterable)
            #pool.join()
            #print ('tile proc finished')

            node_dut.node_run (cycle)
            cycle = cycle + 1

        end = time.time()
        print ('simulation time: ' + str(end-start) + 'secs')

        # For DEBUG only - dump the contents of all tiles
        # NOTE: Output and input tiles are dummy tiles to enable self-contained simulation
        if (cfg.debug):
            node_dump(node_dut, self.tracepath)

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
        print('Success: Hadrware results compiled!!')

        '''# Compare with GPU results (dynamic energy only)
        dpe_energy_l1 = metric_dict['total_energy']
        print (str (dpe_energy_l1) + ' joules')

        gpu_leak = 16 #watt
        gpu_tot = 51
        gpu_time_l1 = 0.629 / 1000
        dpe_time_l1 = metric_dict['time']
        gpu_energy_l1 = (gpu_tot)*gpu_time_l1

        print ('energyX', str (gpu_energy_l1/dpe_energy_l1))
        print ('timeX', str (gpu_time_l1/dpe_time_l1))'''

        # Analyze the recorder xbar currents
        #print ('Analyzing recorded xbar currents')
        #record_xbar (node_dut)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--net", help="The net name as it is in test/testasm.", default='char_rnn')
    args = parser.parse_args()
    net = args.net

    print('Input net is {}'.format(net))
    DPE(net).run()
