# Defines all the components needed by a tile
# IMA, EDRAM, EDRAM controller

import sys
import config as cfg
import constants as param
import ima_modules
from ima_modules import int2bin

# function to check keys match between two dictionaries
def dict_match (dict1, dict2):
    for keyone in dict1.keys():
        if keyone not in dict2.keys():
            return 0
    return 1

# an instruction memory to store the tile instructions
class instrn_memory (ima_modules.instrn_memory):
    def write (self, addr, data):
        self.num_access += 1
        assert (type(addr) == int), 'addr type should be int'
        assert (self.addr_start <= addr <= self.addr_end), 'addr exceeds the memory bounds'
        assert ((dict_match(data, param.dummy_instrn_tile) == 1) and \
                (len(data) == constants.data_width)), 'data should be a dict if tile_instrn_dummy type'
        self.memfile[addr - self.addr_start] = data

# adding a receive buffer (full-assoc cache (tag = neuron_id)) to enable non-blocking receives
class receive_buffer (object):
    def __init__ (self, buff_size):
        # define num_access
        self.num_access = 0

        # define latency
        #self.latency = param.receive_buffer_lat
        self.latency = 0

        # Consists of a list of dictionaries (data, neuron_id)
        temp_rb_list = [''] * cfg.receive_buffer_width
        temp_dict = {'data': temp_rb_list[:], 'valid': 0}
        self.buffer = []
        for i in range (buff_size):
            self.buffer.append (temp_dict.copy())
        self.rd_ptr = 0
        self.wr_ptr = 0

    # access (read/write) latency for receive_buffer
    def getLatency (self):
        return self.latency

    # invalidates all entries
    def inv (self):
        #self.num_access += 1
        for temp_dict in self.buffer:
            temp_dict['valid'] = 0

    # checks if buffer is empty
    def isempty (self, vtile_id): # each entry in buffer serves a unique vtile
        if (self.buffer[vtile_id]['valid']):
            return 0
        return 1

    # write the data coming from router to buffer if non-full
    def write (self, vtile_id, list_entry):
        assert (vtile_id <= cfg.receive_buffer_depth), 'vtile_id must be less than #receive buffer depth'
        assert (type(list_entry) == list), 'data written to receive buffer should be a list of neuron values'
        if (self.isempty(vtile_id)): # check if receive buffer is empty
            self.num_access += 1
            self.buffer[vtile_id]['data'] = list_entry[:]
            self.buffer[vtile_id]['valid'] = 1
            return 1
        return 0

    # read the value from buffer if tag matches - else stall receive instruction
    def read (self, vtile_id):
        if (not self.isempty(vtile_id)):
            self.num_access += 1
            self.buffer[vtile_id]['valid'] = 0
            return [1, self.buffer[vtile_id]['data'][:]]
        return [0, 0] # tag-hit, data

# a memory instance for edram - edram reads and writes multiple neuron values (based on memory bandwidth)
class edram (ima_modules.memory):

    def getLatency (self):
        return param.edram_lat

    # redefine read - for multiple reads
    def read (self, addr, width = 1): # read edram_buswidth/data_width of continuous reads from edram
        self.num_access += 1
        assert (type(addr) == int), 'addr type should be int'
        assert (self.addr_start <= addr <= self.addr_end), 'addr exceeds the memory bounds'
        # returns  a list of entries (list has one entry - Typical case)
        assert (width < cfg.edram_buswidth/cfg.data_width+1), \
                'read edram width exceeds'
        return self.memfile[(addr - self.addr_start) : \
                (addr - self.addr_start + width)][:]

    # redefine the write assertion
    def write (self, addr, data, width = 1): # write (edram_buswidth/data_width) to continuous writes to edram
        self.num_access += 1
        #print (addr)
        assert (type(addr) == int), 'addr type should be int'
        assert (self.addr_start <= addr <= self.addr_end), 'addr exceeds the memory bounds'
        #assert ((type(data) ==  str) and (len(data) == cfg.edram_buswidth)), \
        #        'data should be a string with edram_datawidth bits'
        assert (type(data) == list), 'edram write data should be a list'
        assert (width < cfg.edram_buswidth/cfg.data_width+1), \
                'write data width exceeds'
        # writes to more than one entires (1 entry - typical case)
        for i in range (width):
            self.memfile[addr + i - self.addr_start] = data[i]


# edram controller includes edram too
class edram_controller (object):
    def __init__ (self):
        # define num_access
        self.num_access = 0
        self.num_access_counter = 0

        # Instantiate EDRAM, valid and counter fields
        self.mem  = edram (cfg.edram_size*1024*8/(cfg.data_width)) #edram_size is in KB
        self.valid  = [0] * (cfg.edram_size*1024*8/(cfg.data_width)) #edram_size is in KB
        self.counter  = [0] * (cfg.edram_size*1024*8/(cfg.data_width)) #edram_size is in KB

        # Define latency
        self.latency = param.edram_lat

        # Last served IMA
        self.lastIdx = -1

    def getLatency (self):
        return self.latency

    # Based on the arbitration logic, decide which ima will be served
    def find_next (self, ren_list, wen_list):
        if (len(ren_list) > 1):
            if ((1 in ren_list[self.lastIdx+1:]) or (1 in wen_list[self.lastIdx+1:])):
                idx1 = ren_list[self.lastIdx+1:].index(1) if any(ren_list[self.lastIdx+1:]) \
                        else param.infinity
                idx2 = wen_list[self.lastIdx+1:].index(1) if any(wen_list[self.lastIdx+1:]) \
                        else param.infinity
                return (self.lastIdx+1) + min (idx1, idx2)
            else:
                idx1 = ren_list[0:self.lastIdx+1].index(1) if any(ren_list[0:self.lastIdx+1]) \
                        else param.infinity
                idx2 = wen_list[0:self.lastIdx+1].index(1) if any(wen_list[0:self.lastIdx+1]) \
                        else param.infinity
                return min (idx1, idx2)
        else: # for one IMA case only
            return 0

    def propagate (self, ren_list, wen_list, rd_width_list, wr_width_list, ramstore_list, addr_list):

        self.num_access += 1
        # check if any wen or ren siganl is active
        assert (any(ren_list) or any(wen_list)), 'atleast one memory access should be present'

        # Traverse the WEN(s) and REN(s) to find the ima to be served
        found = 0
        count = 0
        while (found == 0 and count < cfg.num_ima):
            count = count + 1
            # choose the ima to be served
            idx = self.find_next (ren_list, wen_list)
            assert (idx < cfg.num_ima), 'Find Error: IMA Index not possible'
            self.lastIdx = idx # update last index

            # based on ren and wen perfrom the required action
            assert ((ren_list[idx] ^ wen_list[idx]) == 1), \
                    'Ram Access Error: both ren and wen cannot be same'

            # Check for valid (invalid) for LD (ST)
            if ((self.valid[addr_list[idx]] and ren_list[idx]) or \
                    ((not self.valid[addr_list[idx]]) and wen_list[idx])):
                found = 1

        # Once idx found complete ren/wen operation
        addr = addr_list[idx]
        if (ren_list[idx] == 1): # LD instrcution
            if (found): # change state only if an idx was found
                self.num_access_counter += 1
                for i in range (rd_width_list[idx]):
                    # update the counter & valid flags accordingly
                    self.counter[addr+i] = self.counter[addr+i] - 1
                    if (self.counter[addr+i] <= 0): #modified
                        self.valid[addr+i] = 0
            # read the data and send to ima - if found is 0, ramload is junk
            ramload = self.mem.read (addr, rd_width_list[idx])
            return [found, idx, ramload]

        else: # ST instruction
            if (found): # change state only if an idx was found
                self.num_access_counter += 1
                data = ramstore_list[idx][1][:] # 2nd element of list is data_list
                counter = ramstore_list[idx][0]
                self.mem.write (addr, data, wr_width_list[idx])
                for i in range (wr_width_list[idx]):
                    self.valid[addr+i] = 1
                    self.counter[addr+i] = int(counter)
            return [found, idx, '']

