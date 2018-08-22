## API to dump the contents of a node onto trace files
# Each tile has its own memsim.txt file
# memsim contains all memory contents
#   1. EDRAM
#   2. IMA's data memory
#   3. IMA's xbar input memory
#   4. IMA's xbar output memory

import sys
sys.path.insert (0, '/home/michael/hp_dpe/dpe_emulate-br/include')

from data_convert import *
import config as cfg

# define a dump function for a generic memory entity
def mem_dump (fid, memfile, name, node = '', tile_id = ''):
    assert (type(memfile) == list), 'memfile should be list'
    fid.write (name + ' contents\n')

    for addr in range(len(memfile)):
        # to print in float format
        if (memfile[addr] != ''):
            temp_val = fixed2float (memfile[addr], cfg.int_bits, cfg.frac_bits)
            # use this for debugging/viewing addresses
            #temp_val = bin2int (memfile[addr], cfg.num_bits)
        else:
            temp_val = 0.0
        if (name == 'EDRAM' and (node != '') and (tile_id != '')): # for EDRAM also show counter/valid
            fid.write ('valid: ' + str(node.tile_list[tile_id].edram_controller.valid[addr]) \
                    + ' | counter: ' + str(node.tile_list[tile_id].edram_controller.counter[addr]) + ' | ')
        fid.write(str(temp_val) + '\n')
        # to print in fixed forrmat (binary) -- use this
        #fid.write(entry + '\n')

def node_dump (node, filepath = ''):
    assert (filepath != ''), 'Debug flag is set, filepath cannot be nil'
    for i in range(len(node.tile_list)):
        print('Dumping tile #{}'.format(i))
        filename = filepath + 'tile' + str(i) + '/memsim1.txt'
        fid = open (filename, 'w')

        # dump the edram - one per tile
        mem_dump (fid, node.tile_list[i].edram_controller.mem.memfile, 'EDRAM', node, i)

        # dump the memory components of IMA
        for j in range (len(node.tile_list[0].ima_list)):
            # dump the datamemory
            fid.write ('IMA id: ' + str(j) + '\n')
            mem_dump (fid, node.tile_list[i].ima_list[j].dataMem.memfile, 'DataMemory')

            for k in range (len(node.tile_list[0].ima_list[0].xb_inMem_list)):
                # dump the xbar input memory
                mem_dump (fid, node.tile_list[i].ima_list[j].xb_inMem_list[k].memfile, 'Xbar Input Memory')
                # dump the xbar output memory
                mem_dump (fid, node.tile_list[i].ima_list[j].xb_outMem_list[k].memfile, 'Xbar Output Memory')

        fid.close()

