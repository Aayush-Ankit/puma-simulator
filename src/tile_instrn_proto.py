# Define the instruction prototypes which will be used by the generate_instrn.py file
import sys

import numpy as np
import include.config as cfg
import include.constants as param

# Define instruction prototypes
# generate receive prototype
def i_receive (mem_addr, vtile_id, receive_width, counter, vec = 1):
    i_temp = param.dummy_instrn_tile.copy()
    i_temp['opcode'] = 'receive'
    i_temp['mem_addr'] = mem_addr
    i_temp['vtile_id'] =  vtile_id
    i_temp['r1'] = receive_width
    i_temp['r2'] = counter
    i_temp['vec'] = vec
    return i_temp

# generate send prototype
def i_send (mem_addr, vtile_id, send_width, target_addr, vec = 1):
    i_temp = param.dummy_instrn_tile.copy()
    i_temp['opcode'] = 'send'
    i_temp['mem_addr'] = mem_addr
    i_temp['vtile_id'] = vtile_id
    i_temp['r1'] = send_width
    i_temp['r2'] = target_addr
    i_temp['vec'] = vec
    return i_temp

# generate halt prototype
def i_halt ():
    i_temp = param.dummy_instrn_tile.copy()
    i_temp['opcode'] = 'halt'
    return i_temp



