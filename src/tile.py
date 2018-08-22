# Defines a configurable tile with its methods

import sys, json
sys.path.insert (0, '/home/michael/hp_dpe/dpe_emulate-br/include')

import Queue

import numpy as np
import config as cfg
import constants as param
import ima as ima
import tile_modules as tmod

# IMA specific modules (should not be needed)
import ima_modules

class tile (object):

    instances_created = 0

    ### Instantiate different modules in a tile
    def __init__ (self):

        # Assign a tile_id for identification purpose in debug trace
        self.tile_id = tile.instances_created
        tile.instances_created += 1

        ## Objects which correspond to a hardware component (at least NOW!)
        # ima_list
        self.ima_list = []
        for i in range (cfg.num_ima):
            temp_ima = ima.ima ()
            self.ima_list.append(temp_ima)
        # EDRAM controller (icnludes edram)
        self.edram_controller = tmod.edram_controller ()
        # intruction memory
        self.instrn_memory = tmod.instrn_memory (cfg.tile_instrnMem_size)
        # receive buffer
        self.receive_buffer = tmod.receive_buffer (cfg.receive_buffer_depth)
        # program counter
        self.pc = 0
        # fetched instruction
        self.instrn = param.dummy_instrn_tile

        ## Book-keeping variables (may not have a harwdare relevance)
        # send_queue - part of NOC that connects the tiles
        self.send_queue = Queue.Queue()
        # track instruction being executed hasn't completed yet or not
        self.stall = 0
        # latch tag_hit and data (prevents unnecessary repeated buff accesses)
        self.tag_matched = 0
        self.received_data = []
        # halt for tile
        self.tile_halt = 0
        # for imas
        # tracks the halts of ima all IMAs halt
        self.halt_list = []
        self.ima_nma_list = [] # tells which ima would be running
        # File list for IMA tracefiles
        self.fid_list = []
        # For edram interface (send/receive generated edram accesses)
        self.latency_sr = 0
        self.stage_cycle_sr = 0
        self.vec_count = 0
        # For edram controller (ima generated edram accesses)
        self.memstate = 'free' # can be free/busy
        self.latency = 0 # holds latency for memory access
        self.stage_cycle = 0 # holds current cycle invested in memory access

        # used to calculate leakage energy (power-gated tiles - before they start and after they halt)
        self.cycle_count = 0


    ### Initialize the tile (all IMAs in the tile)
    def tile_init (self, instrnpath, tracepath):
        # Initialize the tile instruction memory
        instrn_filepath = instrnpath + 'tile_imem' + '.npy'
        dict_list = np.load(instrn_filepath)
        self.instrn_memory.load (dict_list)

        # Initialize the IMAs and their trace file ids
        for i in range (cfg.num_ima):
            # tracefile is where stats are dumped
            tracefile = tracepath + 'ima_trace' + str(i) + '.txt'
            fid_temp = open (tracefile, 'w')
            self.fid_list.append (fid_temp)
            # instrn_file provides the instrn_list that the IMA will execute
            instrnfile = instrnpath + 'core_imem' + str(i) + '.npy'
            self.ima_list[i].pipe_init (instrnfile, self.fid_list[i])

        # Initialize the EDRAM - invalidate all entries (valid_list)
        self.edram_controller.valid = [0] * (cfg.edram_size*1024/(cfg.data_width/8))

        # Intiialize the receive buffer - invalidate
        self.receive_buffer.inv ()
        # Initialize the program counter
        self.pc = 0
        self.vec_count = 0
        # Intialize tile
        self.tile_halt = 0
        # Initiaize the halt list & stall flag for tile
        self.halt_list = [0] * cfg.num_ima
        self.ima_nma_list = [1] * cfg.num_ima
        self.stall = 0
        self.cycle_count = 0


    ### Simulate one cycle exectution of all IMAs (which have't halted) & their EDRAM interactions
    def tile_compute (self, cycle):
        ## Simulate a cycle if IMA(s) that haven't halted
        if (not all(self.halt_list)): # A tile halts whwn all IMAs (within the tile) halt
            for i in range (cfg.num_ima):
                if ((not self.halt_list[i]) and self.ima_nma_list[i]):
                    self.ima_list[i].pipe_run (cycle, self.fid_list[i])
                    self.halt_list[i] = self.ima_list[i].halt # update halt

        ## Simulate a cycle of memory operation
        # Probe IMA mem_interface to find one/many pending memory requests
        ren_list = [0] * cfg.num_ima
        wen_list = ren_list[:]
        rd_width_list = ren_list[:]
        wr_width_list = ren_list[:]
        ramstore_list = [''] * cfg.num_ima
        addr_list = ren_list[:]
        for i in range (cfg.num_ima):
            ren_list[i] = self.ima_list[i].mem_interface.ren
            wen_list[i] = self.ima_list[i].mem_interface.wen
            rd_width_list[i] = self.ima_list[i].mem_interface.rd_width
            wr_width_list[i] = self.ima_list[i].mem_interface.wr_width
            addr_list[i] = self.ima_list[i].mem_interface.addr
            ramstore_list[i] = self.ima_list[i].mem_interface.ramstore

        # Invoke memory request if memory is free
        if (self.memstate == 'free' and self.stage_cycle == 0 and (any (ren_list) or any (wen_list))):
            self.memstate = 'busy'
            self.latency = self.edram_controller.getLatency ()
            self.stage_cycle = self.stage_cycle + 1
            # For DEUG only
            #print ('memory controller enters BUSY')

            # check if the access lateny is 2 cycles - need to update ima mem_interface
            if (self.stage_cycle == self.latency - 1):
                [found, idx, ramload] = self.edram_controller.propagate (ren_list, \
                        wen_list, rd_width_list, wr_width_list, ramstore_list, addr_list)

                if (found): # edram controller returns after finisning the LD/ST
                    self.ima_list[idx].mem_interface.wait = 0
                    self.ima_list[idx].mem_interface.ren = 0
                    self.ima_list[idx].mem_interface.wen = 0
                    self.ima_list[idx].mem_interface.ramload = ramload

            #### This case NEEDS FIXING!!
            # check if access latency is 1 cycle - need to complete execute in this cycle
            elif (self.stage_cycle == self.latency):
                # finish & free up edram controller
                self.stage_cycle = 0
                self.memstate = 'free'

                # update memory interface of served ima
                [found, idx, ramload] = self.edram_controller.propagate (ren_list, \
                        wen_list, rd_width_list, wr_width_list, ramstore_list, addr_list)

                if (found): # edram controller returns after finisning the LD/ST
                    self.ima_list[idx].mem_interface.wait = 0
                    self.ima_list[idx].mem_interface.ren = 0
                    self.ima_list[idx].mem_interface.wen = 0
                    self.ima_list[idx].mem_interface.ramload = ramload

                    # do a cycle (finish in case of ST) of execute pipeline stage of the served ima
                    # Note - update_ready fo execute stage is always 1 (Current Deisgn)
                    ex_op = self.ima_list[idx].de_opcode
                    sId = 2
                    if (ex_op == 'st'):
                        do_execute (self, ex_op)
                        self.ima_list[idx].stage_done[sId] = 1
                        self.ima_list[idx].stage_cycle[sId] = 0
                        self.ima_list[idx].stage_empty[sId] = 1
                    # Assumption - DataMemory cannot be done in the last access cycle
                    elif (ex_op == 'ld'):
                        self.stage_cycle[sId] = self.latency[sId] - self.ima_list[0].dataMem.getLatency () # can be data_mem too

        elif (self.memstate == 'busy'): # busy state
            # Update ima mem interface of ima a cycle before finishing
            if (self.stage_cycle == self.latency - 2):
                self.stage_cycle = self.stage_cycle + 1
                [found, idx, ramload] = self.edram_controller.propagate (ren_list, \
                        wen_list, rd_width_list, wr_width_list, ramstore_list, addr_list)

                if (found): # edram controller returns after finisning the LD/ST
                    self.ima_list[idx].mem_interface.wait = 0
                    self.ima_list[idx].mem_interface.ren = 0
                    self.ima_list[idx].mem_interface.wen = 0
                    self.ima_list[idx].mem_interface.ramload = ramload

            # Finish the access and free up controller from previous access
            elif (self.stage_cycle == self.latency -1):
                self.stage_cycle = 0
                self.memstate = 'free'
                #print ('memory controller FREE')

            # Wait for request to finish
            else:
                self.stage_cycle = self.stage_cycle + 1


    ### tile_run - simulate a cycle of execution of the tile
    # data addition to receive buffer happens by the higher level hierarchy
    # ?? - All memory access parts will be modified (based on changes in edram_controller)
    def tile_run (self, cycle, fid):
        self.cycle_count += 1
        ## execute the current instruction in tile's instruction memory
        # Fetch a new instrn only after the previous instrn completes
        if (not self.stall and not self.tile_halt):
            self.instrn = self.instrn_memory.read (self.pc)
            self.pc = self.pc + 1

        # Check if the current fetched instrn can  be completed
        # For DEBUG only
        assert (self.instrn['opcode'] in param.op_list_tile), 'Tile: unsupported opcode'
        if (self.instrn['opcode'] == 'send'):
            # check if the mem_addr is valid
            send_width = self.instrn['r1']
            mem_addr = self.instrn['mem_addr'] + self.vec_count*send_width
            assert (send_width <= cfg.receive_buffer_width), 'Send width must be sm/eq to rec_buff_width'
            if (all (self.edram_controller.valid[mem_addr:mem_addr+send_width])): #check if all data (to be sent) is valid
                # first but not last cycle of edram access
                if (self.stage_cycle_sr == 0 and self.edram_controller.getLatency() != 1):
                    # modify this based on edram bandwidth and send width ???
                    self.latency_sr = self.edram_controller.getLatency ()
                    self.stage_cycle_sr += 1
                    self.stall = 1
                # last cycle of edram access
                elif (self.stage_cycle_sr == self.latency_sr - 1 or self.edram_controller.getLatency() == 1):
                    # reset the stage_cycle
                    self.stage_cycle_sr = 0
                    # add the entry to send list (send_list is physically part of NOC and not tile)
                    vtile_id = self.instrn['vtile_id']
                    target_addr = self.instrn['r2'] # (node_id+tile_id)
                    #data = [''] * send_width
                    #for i in range (send_width):
                    #    temp_data = self.edram_controller.mem.read(mem_addr+i)
                    #    data[i] = temp_data
                    data = self.edram_controller.mem.read(mem_addr, send_width)
                    temp_dict = {'data':data[:], 'target_addr':target_addr, 'cycle':cycle, 'vtile_id':vtile_id}
                    self.send_queue.put (temp_dict)
                    # update the counter and valid flag (if req.) for edram
                    # should add some sort of edram_propagate (this adds to energy as well) ???
                    for i in range (send_width):
                        self.edram_controller.counter[mem_addr+i] -= 1
                        if (self.edram_controller.counter[mem_addr+i] <= 0):
                            self.edram_controller.valid[mem_addr+i] = 0
                    # send vector instruction completes
                    if (self.vec_count == self.instrn['vec']-1):
                        self.vec_count = 0
                        self.stall = 0
                    # a unit of vector send finishes
                    else:
                        self.vec_count += 1
                # other cycles (not first or last)
                else:
                    self.stage_cycle_sr += 1
            # stall if edram entry is not empty
            else:
                self.stall = 1

        elif (self.instrn['opcode'] == 'receive'):
            # check hit if only if not checked previously
            if (self.tag_matched == 0): # tag_matched - basically a read hit in receive_buffer
                # receive_buffer operation in its last cycle
                if ((self.stage_cycle_sr == 0 and self.receive_buffer.getLatency() == 0) or \
                    (self.stage_cycle_sr == self.receive_buffer.getLatency())):
                    self.stage_cycle_sr = 0
                    vtile_id = self.instrn['vtile_id']
                    [tag_hit, data] = self.receive_buffer.read (vtile_id)
                    self.tag_matched = tag_hit if (vtile_id >= 0) else 1 # else case receive a dumy data (eg: padding data in conv)
                    self.received_data = data
                else:
                    self.stage_cycle_sr += 1

            receive_width = self.instrn['r1']
            mem_addr = self.instrn['mem_addr'] + self.vec_count * receive_width
            # if tag matches check if edram entry is empty/free (invalid)
            empty = 1
            # check if all mem_addr entries are invalid/empty
            for i in range (receive_width):
                if (self.edram_controller.valid[mem_addr+i] == 1):
                    empty = 0
                    break
            #if (self.tag_matched and (not all(self.edram_controller.valid[mem_addr:mem_addr+receive_width]))):
            if (self.tag_matched and empty):
                assert (self.instrn['vtile_id'] >= 0 and receive_width == len(self.received_data)), 'receive_width & send widths mismatch'
                # first but not last cycle of edram access
                if (self.stage_cycle_sr == 0 and self.edram_controller.getLatency() != 1):
                    self.latency_sr = self.edram_controller.getLatency ()
                    self.stage_cycle_sr += 1
                    self.stall = 1
                # last cycle of edram access
                elif (self.stage_cycle_sr == self.latency_sr - 1 or self.edram_controller.getLatency() == 1):
                    # reset the stage_cycle
                    self.stage_cycle_sr = 0
                    # write data to edram and set valid &counter entries
                    if (self.instrn['vtile_id'] < 0): #adding support for zero receive
                        self.received_data = [cfg.num_bits * '0'] * receive_width
                    temp_counter = self.instrn['r2']
                    self.edram_controller.mem.write (mem_addr, self.received_data, receive_width)
                    for i in range (receive_width):
                        #self.edram_controller.mem.write (mem_addr+i, self.received_data[i])
                        # should add some sort of edram_propagate (this adds to energy as well) ???
                        self.edram_controller.valid[mem_addr+i] = 1
                        self.edram_controller.counter[mem_addr+i] = temp_counter
                    # set other book-keeping flags
                    if (self.vec_count == self.instrn['vec']-1):
                        self.vec_count = 0
                        self.tag_matched = 0
                        self.stall = 0
                    else:
                        self.tag_matched = 0
                        self.vec_count += 1
                # other cycles (not first or last)
                else:
                    self.stage_cycle_sr += 1
            else:
                self.stall = 1

        # This feature has been deprecated
        elif (self.instrn['opcode'] == 'compute'):
            ## mask tells which new ima(s) should start executing
            ## note: some ima(s) could have already been running previously
            temp_ima_nma = self.instrn['ima_nma']  # this is a bit-string # This does nothing
            #for i in range (cfg.num_ima):
            #    self.ima_nma_list[i] = self.ima_nma_list[i] | int(temp_ima_nma[i])

        else: # halt instruction
            # tile can halt only after all imas halt
            # those imas which haven't been used don't matter
            for k in range(len(self.halt_list)):
                if (not self.ima_nma_list[k]):
                    self.halt_list[k] = 1

            # check if all imas halted and send_queue is empty
            if (all(self.halt_list) and self.send_queue.empty()):
                self.tile_halt = 1

                # Close all ima the trace files
                for tr_fid in self.fid_list:
                    tr_fid.close ()
                    self.stall = 0 # Doesn't matter as this was the last cycle

                # Update the tile trace
                if (cfg.debug):
                    fid.write ('Tile ran for ' + str(cycle) + ' cycles')
            else:
                # prevent new instructions to befetched
                self.stall = 1

        ## simulate a cycle of ima execution based on current state of self.ima_nma
        self.tile_compute (cycle)

        ## for DEBUG only
        if (cfg.debug and (not self.tile_halt)):
            fid.write ('cycle: ' + str(cycle) + '   |   instrn: ' + self.instrn['opcode'] + '   |   \
addr: ' + str(self.instrn['mem_addr']) + '   |   vtileId: ' + str(self.instrn['vtile_id']) + '   |   ima_halt_list: ')
            json.dump (self.halt_list, fid)
            fid.write ('\n')
