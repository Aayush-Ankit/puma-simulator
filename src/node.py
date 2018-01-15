# Defines a configurable node with its methods
import sys, getopt
sys.path.insert (0, '/home/aa/dpe_emulate/include/')
sys.path.insert (0, '/home/aa/dpe_emulate/src/')

import numpy as np
import config as cfg
import constants as param
import ima_modules
import ima
import tile_modules
import tile
import node_modules as nmod

class node (object):

    instances_created = 0

    ### Instantiate different modules in a node
    def __init__ (self):

        # Assign a node_id for identification purpose in debug trace
        self.node_id = node.instances_created

        # Instantiate the tile list
        self.tile_list = []
        for i in range (cfg.num_tile): #first & last tiles - dummy, others - compute
            temp_tile = tile.tile ()
            self.tile_list.append (temp_tile)

        # Instantiate the NOC
        self.noc = nmod.noc ()

        # Some book-keeping variables (Can have harwdare correspondance)
        self.node_halt = 0
        self.tile_halt_list = [0] * cfg.num_tile
        self.tile_fid_list = []

        self.noc_start = 0


    ### Initialize the tiles within node and open the trace file for each tile
    def node_init (self, instrnpath, tracepath):
        for i in range (cfg.num_tile):
            # open tracefile for tile - place where stats are dumped
            tracefile = tracepath + 'tile' + str(i) + '/tile_trace.txt'
            fid_temp = open (tracefile, 'w')
            self.tile_fid_list.append (fid_temp)

            # initialize the tile
            temp_instrnpath = instrnpath + 'tile' + str(i) + '/'
            temp_tracepath = tracepath + 'tile' + str(i) + '/'
            self.tile_list[i].tile_init (temp_instrnpath, temp_tracepath)

        # intialize the tile_halt_list and node_halt
        self.node_halt = 0
        self.tile_halt_list = [0] * cfg.num_tile

    ## A cyle execution of each tile and probe each tile's halt
    #def node_tile_run (self, cycle, i):
    #    print ('running tile', i)
    #    #run a tile if not halted
    #    if (not self.tile_list[i].tile_halt):
    #        self.tile_list[i].tile_run (cycle, self.tile_fid_list[i])
    #        self.tile_halt_list[i] = self.tile_list[i].tile_halt


    ### Simulate a cycle of execution of a node
    def node_run (self, cycle):

        # data transfer latency includes noc latency and receive buffer latency
        #transfer_latency = self.noc.getLatency() + \
        #        self.tile_list[0].receive_buffer.getLatency()


        # A cyle execution of each tile and probe each tile's halt
        for i in range (cfg.num_tile):
            # run a tile only if has not halted
            if (not self.tile_list[i].tile_halt):
                self.tile_list[i].tile_run (cycle, self.tile_fid_list[i])
                self.tile_halt_list[i] = self.tile_list[i].tile_halt

        # Start noc based on send_queue of all tiles - one non-empty
        if (self.noc_start == 0):
            for i in range (cfg.num_tile):
                if (not self.tile_list[i].send_queue.empty()):
                    self.noc_start = 1
                    self.noc.start_noc (cycle)
                    break

        # Stop noc based on send_queue of all tiles -- all empty
        if (self.noc_start == 1):
            count = 0
            for i in range (cfg.num_tile):
                if (not self.tile_list[i].send_queue.empty()):
                    count += 1
                    break
            if (count == 0):
                self.noc.stop_noc (cycle)
                self.noc_start = 0

        # A cycle execution of noc (data transfers between tiles)
        # If latency satisfies, write to destination tile's receive buffer
        for i in range (cfg.num_tile):
            # check entry at head of queue (if non-empty) for all tiles for noc latency
            if (not self.tile_list[i].send_queue.empty()):
                temp_queue_head = self.tile_list[i].send_queue.queue[0]
                target_addr = temp_queue_head['target_addr']
                transfer_latency = self.noc.getLatency (target_addr, i) + \
                        self.tile_list[0].receive_buffer.getLatency()
                if (((cycle - temp_queue_head['cycle']) >= transfer_latency-1)):
                    # attempt to write to destination's receive buffer
                    tile_addr = self.noc.propagate (target_addr, i)
                    temp_data = temp_queue_head['data'][:]
                    temp_vtile_id = temp_queue_head['vtile_id']
                    #print (tile_addr)
                    write_hit = self.tile_list[tile_addr].receive_buffer.write (temp_vtile_id, temp_data)
                    # if write is success - remove from queue
                    if (write_hit == 1):
                        self.tile_list[i].send_queue.get()
                        # added to get HT counts
                        self.noc.propagate_count (target_addr, i)

        # For DEBUG
        #if (cycle%5000 == 0):
        print ('Cycle: ', cycle, 'Tile halt list', self.tile_halt_list)

        # check if node halted
        if (all (self.tile_halt_list)):
            self.node_halt = 1
            for tr_id in self.tile_fid_list:
                tr_id.close ()
            print ('cycle: ' + str (cycle) + ' Node Halted')

