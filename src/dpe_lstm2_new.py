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


## Import constituent modeles/dependencies
import sys, getopt, os

import torchfile as tf
from data_convert import *
from node_dump import *
import numpy as np

import constants as param
import ima_modules
import ima
import tile_modules
import tile
import node_modules
import node


## Set the instruction & trace paths (create the folder hierarchy)
# Assumption: All instructions for all TILEs and IMAs have already been generated
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
instrndir = os.path.join(root_dir, "test/testasm/")
tracedir = os.path.join(root_dir, "test/traces/")

assert (os.path.exists(instrndir) == 1), 'Instructions for net missing: generate intuctions (in folder hierarchy) hierarchy'
'''if not os.path.exists(instrndir):
    os.makedirs(instrndir)
    for i in range (param.num_tile):
        temp_tiledir = instrndir + '/tile' + str(i)
        os.makedirs(temp_tiledir)'''

if not os.path.exists(tracedir):
    os.makedirs(tracedir)
    for i in range (param.num_tile):
        temp_tiledir = tracedir + '/tile' + str(i)
        os.makedirs(temp_tiledir)

instrnpath = instrndir + '/'
tracepath = tracedir + '/'


## Instantiate the node under test
# A physical node consists of several logical nodes equal to the actual node size
node_dut = node.node ()


## Initialize the node with instrn & trace paths
# instrnpath provides instrns for tile & resident imas
# tracepath is where all tile & ima traces will be stored
node_dut.node_init (instrnpath, tracepath)


## Read the input data (input.t7) into the input tile's edram(controller)
inp_filename = instrnpath + 'input.t7'
inp_tileId = 0
print (os.path.exists (inp_filename))
assert (os.path.exists (inp_filename) == True), 'Input Error: Provide inputbefore running the DPE'
inp = tf.load (inp_filename)
for i in range (len(inp.data)):
    data = float2fixed (inp['data'][i], param.int_bits, param.frac_bits)
    node_dut.tile_list[inp_tileId].edram_controller.mem.memfile[i] = data
    node_dut.tile_list[inp_tileId].edram_controller.counter[i]     = int(inp['counter'][i])
    node_dut.tile_list[inp_tileId].edram_controller.valid[i]       = int(inp['valid'][i])


## Program DNN weights on the xbars
# torch table in file - (tracepath/tile<>/weights/ima<>_xbar<>.t7)
for i in range (1, param.num_tile-1):
    print ('Programming tile no: ', i)
    for j in range (param.num_ima):
        print ('Programming ima no: ', j)
        for k in range (param.num_xbar):
            wt_filename = instrnpath + 'tile' + str(i) + '/weights/' + \
                        'ima' + str(j) + '_xbar' + str(k) + '.t7'
            if (os.path.exists(wt_filename)): # check if weights for the xbar exist
                wt_temp = tf.load (wt_filename)
                node_dut.tile_list[i].ima_list[j].xbar_list[k].program (wt_temp)


## Run all the tiles
cycle = 0
while (not node_dut.node_halt and cycle < param.cycles_max):
    node_dut.node_run (cycle)
    cycle = cycle + 1
print 'Finally node halted' + ' | PS: max_cycles ' + str (param.cycles_max)


## For DEBUG only - dump the contents of all tiles
# NOTE: Output and input tiles are dummy tiles to enable self-contained simulation
if (param.debug):
    node_dump (node_dut, tracepath)


## Dump the contents of output tile (DNN output) to output file (output.txt)
output_file = tracepath + 'output.txt'
fid = open (output_file, 'w')
tile_id  = param.num_tile - 1
mem_dump (fid, node_dut.tile_list[tile_id].edram_controller.mem.memfile, 'EDRAM')
fid.close ()
print 'Output Tile dump finished'


## Dump the harwdare access traces (For now - later upgrade to actual energy numbers)
hwtrace_file = tracepath + 'harwdare_stats.txt'
hw_comp = {'xbar':0,    'dac':0,    'snh':0,        'mux1':0,       'mux2':0,    'adc':0, \
           'alu':0,     'imem':0,   'dmem':0,       'xbInmem':0,    'xbOutmem':0, \
           'imem_t':0,  'rbuff':0,  'edram':0,      'edctrl':0, \
           'noc_intra':0,           'noc_inter':0
           }
fid = open (hwtrace_file, 'w')

# traverse components to populate dict (hw_comp)
hw_comp['noc_intra'] += node_dut.noc.num_access_intra
hw_comp['noc_inter'] += node_dut.noc.num_access_inter

for i in range (1, param.num_tile-1): # ignore dummy (input & output) tiles
    hw_comp['imem_t'] += node_dut.tile_list[i].instrn_memory.num_access
    hw_comp['rbuff'] += node_dut.tile_list[i].receive_buffer.num_access
    hw_comp['edram'] += node_dut.tile_list[i].edram_controller.mem.num_access
    hw_comp['edctrl'] += node_dut.tile_list[i].edram_controller.num_access

    for j in range (param.num_ima):
        for k in range (param.num_xbar):
            hw_comp['xbar'] += node_dut.tile_list[i].ima_list[j].xbar_list[k].num_access

        for k in range (param.num_xbar):
            for l in range (param.xbar_size):
                hw_comp['dac'] += node_dut.tile_list[i].ima_list[j].dacArray_list[k].dac_list[l].num_access

        for k in range (param.num_xbar):
            hw_comp['snh'] += (node_dut.tile_list[i].ima_list[j].snh_list[k].num_access * param.xbar_size) # each snh is
            # basically an array of multiple snhs (individual power in constants file must be for one discerete snh)

        for k in range (param.num_xbar):
            hw_comp['mux1'] += node_dut.tile_list[i].ima_list[j].mux1_list[k].num_access

        for k in range (param.num_xbar / param.num_adc):
            hw_comp['mux2'] += node_dut.tile_list[i].ima_list[j].mux1_list[k].num_access

        for k in range (param.num_adc):
            hw_comp['adc'] += node_dut.tile_list[i].ima_list[j].adc_list[k].num_access

        for k in range (param.num_ALU):
            hw_comp['alu'] += node_dut.tile_list[i].ima_list[j].alu_list[k].num_access

        hw_comp['imem'] += node_dut.tile_list[i].ima_list[j].instrnMem.num_access

        hw_comp['dmem'] += node_dut.tile_list[i].ima_list[j].dataMem.num_access

        for k in range (param.num_xbar):
            hw_comp['xbInmem'] += node_dut.tile_list[i].ima_list[j].xb_inMem_list[k].num_access

        for k in range (param.num_xbar):
            hw_comp['xbOutmem'] += node_dut.tile_list[i].ima_list[j].xb_outMem_list[k].num_access

# Write the dict components to a file for visualization
for key, value in hw_comp.items():
    fid.write (key + ': ')
    fid.write (str(value) + '\n')
fid.close ()
print 'Success: Hadrware results compiled!!'

