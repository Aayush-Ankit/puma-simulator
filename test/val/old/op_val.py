# Validate the outer product algorithm with bit-slicing and signed arithmetic
# Validation with 16-bit integers with 32-bit outer-product is sufficient to validate for 16-bit fixed point for fractional numbers

import sys
import os
import numpy as np

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

from src.data_convert import *

# Specify parameters for testing
num_bits = 16
int_bits = 16
frac_bits = num_bits - int_bits
xbar_bits = 2

# assumed extra bits for accumulation
xbar_extraBits = 7
bias = 2** (xbar_extraBits-1)


# function to slice an unsigned weight into 2-bit chunks (number of weight bits = 2*num_bits)
def wt_bitSlice (wt):
    wt_slice = []
    wt_fixed = float2fixed (wt, int_bits, frac_bits)
    # append zeros to first num_bits
    for i in range (num_bits/2):
        temp = '00'
        temp_int = bin2int(temp,xbar_extraBits+1) + bias
        bias_temp = float2fixed (temp_int, xbar_extraBits, 0)
        wt_slice.append (bias_temp)
    # add wt_fixed bits starting from MSB
    for i in range (num_bits/2):
        temp = wt_fixed[i*xbar_bits:(i+1)*xbar_bits]
        temp_int = bin2int(temp,xbar_extraBits+1) + bias
        bias_temp = float2fixed (temp_int, xbar_extraBits, 0)
        wt_slice.append (bias_temp)

    return wt_slice

# add/sub two fixed point numbers (the numbers are unsigned)
def add_fixed (in1, in2, sub=0):
    in1_float = fixed2float (in1, int_bits, frac_bits)
    in2_float = fixed2float (in2, int_bits, frac_bits)
    if (sub == 0):
        out = in1_float + in2_float
        # cap the output at the maximum (memristor behaviour, staurates at max. positive)
        #if (out > )
    else:
        out = in1_float - in2_float
    #print ('in1: ' + str(in1_float) + ' in2: ' + str(in2_float) + ' out: ' + str(out))
    return float2fixed (out, xbar_extraBits, frac_bits)

# function to multiply two inputs and accumulate over weight using bit-streamed multiplication
def outer_prod (wt_slice, in1_fixed, in2_fixed, sub=0):
    # stream over in1 bits
    for i in range (len(in1_fixed)):
        # compute the 2*num_bits value to be accumulated
        temp = in2_fixed
        if (in1_fixed[-1*(i+1)] == '0'): # lsb is the right-most bit
            temp = num_bits * '0'
        acc = (num_bits-i)*'0' + temp + i*'0' # left shifted for bit-streamed mul
        #print ('Bit pos: ' + str(i) + "acc: " + acc)
        # add respective parts of acc on wt_slice
        for j in range (len(wt_slice)):
            wt_slice[j] = add_fixed (wt_slice[j], acc[j*xbar_bits:(j+1)*xbar_bits], sub)
        #print ('Wt slice: ', wt_slice)

# run crs over wt_slice to give 16-bit weight
def crs (wt_slice):
    val = 0.0
    for i in range (len(wt_slice)):
        shift_pos = 2 * ((len(wt_slice)-1) - i)
        val += (fixed2float (wt_slice[i], 2*int_bits, 2*frac_bits)- bias) * (2**shift_pos)

    return val

# evaluation script
def eval (in1, in2, wt):
    wt_slice = wt_bitSlice (wt)
    # use magnitudes of in1 and in2 - signed magnitude representation
    in1_fixed = float2fixed (abs(in1), int_bits, frac_bits)
    in2_fixed = float2fixed (abs(in2), int_bits, frac_bits)
    sub = 0 if (in1*in2 >= 0) else 1
    #print ('in1_fixed: ' + str(in1_fixed) + ' in2_fixed: ' + str(in2_fixed))

    outer_prod (wt_slice, in1_fixed, in2_fixed, sub)
    val = crs (wt_slice)
    print ('val_exp', wt+in1*in2)
    print ('val_out', val)


## testcases
# Case 1: evaluate for positive integers (num_bits = 16, int_bits = 16)
in1 = 1645
in2 = 232
wt = 2406 # this will always be positive (weight on crossbar is represneted as an unsigned number with bias column)
eval (in1, in2, wt)

# Case 2: evaluate for negative integers (num_bits = 16, int_bits = 16)
# this will always be positive (weight on crossbar is represneted as an unsigned number with bias stored seperately)
in1 = -214
in2 = 178
wt = 50000
eval (in1, in2, wt)


