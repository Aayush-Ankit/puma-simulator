# APIs to convert data from:
# 1. float to fixed point binary (2s complement) [float to bit-string]
# 2. fixed point binary (2s complement) to float [bit-string to float]
# 3. integer to binary (2s complement) [int to bit-string]
# 4. binary (2s complement) to inetger [bit-string to int]
import numpy as np

def bin2int (binary_string, bits):
    #if binary_string == '':
    #    return 0
    val = int (binary_string,2)
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val

def int2bin (int_data, bits):
    data_str = bin(int_data & (2**bits-1))[2:].zfill(bits)
    return data_str

def float2fixed (float_data, int_bits, frac_bits):
    temp = float_data * (2**frac_bits)
    temp = int(round (temp))
    return int2bin (temp, (int_bits+frac_bits))

def fixed2float (binary_string, int_bits, frac_bits):
    temp = bin2int (binary_string, (int_bits + frac_bits))
    return float(temp) / (2**frac_bits)

# defining float (2d numpy float array) <-> fixed (2d list of strings) conversion
def float2fixed_2d (float_data_arr, int_bits, frac_bits):
    (num_row, num_col) = np.shape(float_data_arr)
    # input type - array, outpt type = 2d list
    #out_list = [['']*num_col] * num_row
    out_list = [['' for i in range(num_col)] for j in range(num_row)]
    for i in range (num_row):
        for j in range (num_col):
            float_data = float_data_arr[i,j]
            out_list[i][j] = float2fixed (float_data, int_bits, frac_bits)
    return out_list

# defining fixed (2d list of string) <-> float (2d numpy float array) conversion
def fixed2float_2d (binary_string_list, int_bits, frac_bits):
    (num_row, num_col) = np.shape(binary_string_list)
    # input type - 2d list, outpt type = array
    out_arr = np.zeros((num_row, num_col), dtype=float)
    for i in range (num_row):
        for j in range (num_col):
            binary_string = binary_string_list[i][j]
            out_arr[i, j] = fixed2float (binary_string, int_bits, frac_bits)
    return out_arr

# defiing a fuction to extract a given num of bits from each element of a 2d binary_string_list
def getBitsFromList (binary_string_list, start_bit, num_bit):
    (num_row, num_col) = np.shape(binary_string_list)
    # input type - 2d list, outpt type = 2d list
    out_list = [['']*num_col] * num_row
    for i in range (num_row):
        for j in range (num_col):
            out_list[i][j] = binary_string_list[i][j][start_bit:start_bit + num_bit]
    return out_list


## Obsolete - because they were long and less readable
'''def bin2frac (binary_string):
    result = 0
    ex = 2.0
    for c in binary_string:
        if c == '1':
            result += 1/ex
        ex *= 2
    return result

def frac2bin (frac, bits):
    result = ''
    ex = 2.0
    for i in range (bits):
        frac = frac * ex
        result += str(int(frac))
        frac = frac - int(frac)
    return result

def float2fixed2 (float_data, int_bits, frac_bits):
    temp = abs(float_data)
    int_part = int (temp)
    bin1 = int2bin (int_part, int_bits)
    frac_part = temp - int_part
    bin2 = frac2bin (frac_part, frac_bits)

    if (float_data >= 0):
        return bin1 + bin2
    else:
        result = -1 * int ((bin1 + bin2), 2)
        result = int2bin (result, int_bits + frac_bits)
        return result

def fixed2float2 (binary_string, int_bits, frac_bits):
    if (binary_string[0] == 1):
        print ('aho negative')
        num = -1 * bin2int (binary_string, int_bits + frac_bits) #negative integer
        binary_string = int2bin (num, int_bits + frac_bits)

    return bin2int (binary_string[0:int_bits], int_bits) + \
            bin2frac (binary_string[int_bits:])'''

# Test the above functions
'''import numpy as np
num = 4
int_bits = 4
frac_bits = 12

inp_float = np.random.rand(num)
print ('original: ', inp_float)

inp1 = ['']*num
inp2 = ['']*num
for i in range (num):
    inp1[i] = float2fixed (inp_float[i], int_bits, frac_bits)
    inp2[i] = float2fixed2 (inp_float[i], int_bits, frac_bits)
print ('fixed: ', inp1)
print ('fixed2: ', inp2)

inp_f1 = [0.0]*num
inp_f2 = [0.0]*num
for i in range (num):
    inp_f1[i] = fixed2float (inp1[i], int_bits, frac_bits)
    inp_f2[i] = fixed2float2 (inp2[i], int_bits, frac_bits)
print ('back2float: ', inp_f1)
print ('back2float2: ', inp_f2)'''
