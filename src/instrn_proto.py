# Define the instruction prototypes which will be used by the generate_instrn.py file
import sys
sys.path.insert (0, '/home/aa/dpe_emulate/include')

import numpy as np
from data_convert import *
import config as cfg
import constants as param

# Define nstruction prototypes
# generate load prototype - load data from edram to (datamem/xbinmem)
def i_load (d1, r1, load_width = 1, vec = 1):
    assert (load_width <= (cfg.edram_buswidth/cfg.data_width)), 'Load width must be smaller than \
    edram_buswidth/data_width'
    i_temp = param.dummy_instrn.copy ()
    i_temp['opcode'] = 'ld'
    i_temp['d1'] = d1 # rf addr
    i_temp['r1'] = r1 # mem addr
    i_temp['imm'] = load_width
    i_temp['vec'] = vec
    return i_temp

# generate store protoyype - store data from (datamem/sboutmem) to edram
def i_store (d1, r1, counter = 1, store_width = 1, vec = 1):
    assert (store_width <= (cfg.edram_buswidth/cfg.data_width)), 'Load width must be smaller than \
    edram_buswidth/data_width'
    i_temp = param.dummy_instrn.copy ()
    i_temp['opcode'] = 'st'
    i_temp['d1'] = d1 # mem addr
    i_temp['r1'] = r1 # rf addr
    i_temp['r2'] = counter
    i_temp['imm'] = store_width
    i_temp['vec'] = vec
    return i_temp

# generate cp prototype:
# src_type = 0: copy data from (datamem/xbInmem) to (datmem/xbInmem)
# src_type = 1: copy data from (datamem/xbOutmem) to (datmem/xbInmem)
def i_copy (d1, r1, vec = 1, src_type = 0):
    i_temp = param.dummy_instrn.copy ()
    i_temp['opcode'] = 'cp'
    i_temp['d1'] = d1
    i_temp['r1'] = r1
    i_temp['r2'] = src_type
    i_temp['vec'] = vec
    return i_temp

# generate set prototype - set a particular reg value (datamem/xbInmem) to a scalar
def i_set (d1, imm, vec = 1):
    i_temp = param.dummy_instrn.copy ()
    i_temp['opcode'] = 'set'
    i_temp['d1'] = d1
    i_temp['imm'] = imm if (type(imm) == str) else int2bin(imm, 16)
    i_temp['vec'] = vec
    return i_temp

# generate alu prototype - arithmrtic, logical, non-linear opearrions
def i_alu (aluop, d1, r1, r2=0, imm = 0, vec = 1):
    i_temp = param.dummy_instrn.copy()
    i_temp['opcode'] = 'alu'
    i_temp['aluop'] = aluop
    i_temp['d1'] = d1
    i_temp['r1'] = r1
    i_temp['r2'] = r2
    i_temp['imm'] = imm # will be used in lsh
    i_temp['vec'] = vec
    return i_temp

# generate alui prototype - arithmrtic, logical, non-linear opearrions with scalars
def i_alui (aluop, d1, r1, imm, vec = 1):
    i_temp = param.dummy_instrn.copy()
    i_temp['opcode'] = 'alui'
    i_temp['aluop'] = aluop
    i_temp['d1'] = d1
    i_temp['r1'] = r1
    i_temp['imm'] = imm # will be used in alui
    i_temp['vec'] = vec
    return i_temp

# generate mvm prototype - xbar isntrn
def i_mvm (xb_nma = cfg.num_xbar, r1=0, r2=0): # r1 is displacement, r2 is length of a continuum of data
    i_temp = param.dummy_instrn.copy()
    i_temp['opcode'] = 'mvm'
    i_temp['r1'] = r1
    i_temp['r2'] = r2
    i_temp['xb_nma'] = cfg.num_xbar
    return i_temp

# generate halt prototype
def i_hlt ():
    i_temp = param.dummy_instrn.copy()
    i_temp['opcode'] = 'hlt'
    return i_temp

# generate jmp prototype
def i_jmp (imm): # imm is the jump target
    i_temp = param.dummy_instrn.copy()
    i_temp['opcode'] = 'jmp'
    i_temp['imm'] = imm
    return i_temp

# generate beq prototype
def i_beq (r1, r2, imm): # imm is the jump target
    i_temp = param.dummy_instrn.copy()
    i_temp['opcode'] = 'beq'
    i_temp['r1'] = r1
    i_temp['r2'] = r2
    i_temp['imm'] = imm
    return i_temp

# generate alu_int prototype
def i_alu_int (aluop, d1, r1, r2):
    i_temp = param.dummy_instrn.copy()
    i_temp['opcode'] = 'alu_int'
    i_temp['aluop'] = aluop
    i_temp['d1'] = d1
    i_temp['r1'] = r1
    i_temp['r2'] = r2
    return i_temp
