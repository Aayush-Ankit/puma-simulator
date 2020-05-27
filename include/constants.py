## This file contains the data structures used in differnet hierarchies.
## It also holds power, area and latency numbers of different component used in DPE design
import config as cfg
import math
# Limits the number of cycles an IMA runs in case it doesn't halt
infinity = 100000

#############################################################################################################
## Technology/Other constants for all the modules
#############################################################################################################
# IMA - folliwng parameters are not used currently, will be used when analog functionality is implemented
cycle_time = 1 # in nanoseconds (1ns)
vdd = 0.9
xbar_out_min = -10e-10
xbar_out_max = 1 # think about this - ???

#############################################################################################################
## Define commonly used data structures
#############################################################################################################
# List of supported opcodes for tile
op_list_tile = ['send', 'receive', 'compute', 'halt']

# Instruction format for Tile
dummy_instrn_tile = {'opcode' : op_list_tile[0],
                     'mem_addr': 0,     # send/receive - edram_addr
                     'r1': 0,     # send-send_width, receive-receive_width
                     'r2': 0,     # send-target_addr, receive-counter
                     'vtile_id': 0, # send/receive-neuron_id
                     'ima_nma': '',      # compute - a bit for each ima
                     'vec': 0} # vector width

# List of supported opcodes/aluops for IMA - cp will copy data (from data memory of ima to xbarInmem)
op_list = ['ld', 'cp', 'st', 'set', 'nop', 'alu', 'alui', 'mvm', 'vvo', 'hlt', 'jmp', 'beq', 'alu_int', 'crs']
aluop_list = ['add', 'sub', 'sna', 'mul', 'sigmoid'] # sna is also used by mvm isntruction

# Instruction format for IMA
dummy_instrn = {'opcode' : op_list[0],      # instrn op
               'aluop'  : aluop_list[0],   # alu function
               'd1'     : 0,               # destination
               'r1'     : 0,               # operand1 (stride for mvm)
               'r2'     : 0,               # operand2
               'r3'     : 0,               # operand3 (shift)
               'vec'    : 0,               # vector width
               'imm'    : 0,               # immediate (scalar) data
               'xb_nma' : 0 }              # xbar negative-mask, a xbar evaluates if neg-mask = 1

# List of pipeline stages - in order for IMA
stage_list = ['fet', 'dec', 'ex']
last_stage = 'ex'

#############################################################################################################
# IMA Hierarchy parameters
    # Number of Xbars
    # Crossbar Size
    # Crossbar bits
    # Bit resolution of ADCs and DACs
    # Number of ADCs
    # Number of ALUs
    # Data memory size
    # Size of Xbar in/out memory (Register) is dependent on Xbar size and num_bits
    # Instruction memory size
#############################################################################################################

# IMA component latency/power/area dictionary (all values in ns, mw, mm2)
# XBAR - Models from ISAAC paper
xbar_lat_dict = {'2': {'32' : 32,   # first indexed by xbar_bits then by xbar_size
                       '64' : 64,
                       '128': 128,
                       '256': 256},
                 '4': {'32' : 32,
                       '64' : 64,
                       '128': 128,
                       '256': 256},
                 '6': {'32' : 32,
                       '64' : 64,
                       '128': 128,
                       '256': 256}}

xbar_pow_dict = {'2': {'32' : 0.01875,
                       '64' : 0.075,
                       '128': 0.3,
                       '256': 1.2},
                 '4': {'32' : 0.01875,
                       '64' : 0.075,
                       '128': 0.3,
                       '256': 1.2},
                 '6': {'32' : 0.01875,
                       '64' : 0.075,
                       '128': 0.3,
                       '256': 1.2}}

xbar_area_dict = {'2': {'32' : 1.5625 * 10**(-6),
                       '64' : 6.25 * 10**(-6),
                       '128': 2.5 * 10**(-5),
                       '256': 1.0 * 10**(-4)},
                  '4': {'32' : 1.5625 * 10**(-6),
                       '64' : 6.25 * 10**(-6),
                       '128': 2.5 * 10**(-5),
                       '256': 1.0 * 10**(-4)},
                  '6': {'32' : 1.5625 * 10**(-6),
                       '64' : 6.25 * 10**(-6),
                       '128': 2.5 * 10**(-5),
                       '256': 1.0 * 10**(-4)}}

## New values added for xbar MVM/MTVM, OP (parallel write), serial read/write
# the following is lumped power for xbar inner/outer-product - includes peripherals
xbar_op_lat = 20.0*12.8 # with 4 VFUs
xbar_op_pow = 4.44 * 3.27 / (12.8)

xbar_ip_lat = 100.0
#xbar_ip_pow = (1.37*2.0) # xbar_ip_pow (includes all mvmu)
xbar_ip_pow = (1.37*2.0) - 1.04 # xbar_ip_pow (includes all mvmu except ADC - uncomment num_access for ADC object)

# Note the read and write lat/pow are for entire xbar
xbar_rd_lat = 328.0 * 1000 * (1/32.0)
xbar_wr_lat = 351.0 * 1000 * (1/32.0)

# the following is lumped power for xbar rd/wr (for whole array) - includes peripherals
xbar_rd_pow = 208.0 * 1000 * (1/32.0) / xbar_rd_lat
xbar_wr_pow = 676.0 * 1000 * (1/32.0) / xbar_rd_lat

## Adding power area and latency for Digital MVMU V1 and V2
Digital_xbar_lat_dict = {'Digital_V1': {'32': { '100':130, # first indexed by version then by xbar_size and then by % of non_0 values
                                                '90': 114, # For V1 it is (4n+2)*T and for V2 it is (3n+2+xbar_size)*T
                                                '80': 102, 
                                                '70': 90, 
                                                '60': 78, 
                                                '50': 66, 
                                                '40': 50, 
                                                '30': 38, 
                                                '20': 26, 
                                                '10': 14},      
                                        '64': { '100':258, 
                                                '90': 230,
                                                '80': 206, 
                                                '70': 178, 
                                                '60': 154, 
                                                '50': 130, 
                                                '40': 102, 
                                                '30': 78, 
                                                '20': 50, 
                                                '10': 26},      
                                        '128':{ '100':514,
                                                '90': 462, 
                                                '80': 410, 
                                                '70': 358, 
                                                '60': 306, 
                                                '50': 258, 
                                                '40': 206, 
                                                '30': 154, 
                                                '20': 102, 
                                                '10': 50},     
                                        '256':{ '100':1026, 
                                                '90': 922,
                                                '80': 818, 
                                                '70': 718, 
                                                '60': 614, 
                                                '50': 514, 
                                                '40': 410, 
                                                '30': 306, 
                                                '20': 206, 
                                                '10': 102}},
                         'Digital_V2': {'32' :{ '100':130,
                                                '90': 118,
                                                '80': 109, 
                                                '70': 100, 
                                                '60': 91, 
                                                '50': 82, 
                                                '40': 70, 
                                                '30': 61, 
                                                '20': 52, 
                                                '10': 43},  
                                        '64' :{ '100':258,
                                                '90': 237,  
                                                '80': 219, 
                                                '70': 198, 
                                                '60': 180, 
                                                '50': 162, 
                                                '40': 141, 
                                                '30': 123, 
                                                '20': 102, 
                                                '10': 84},
                                        '128':{ '100':514,
                                                '90': 475,  
                                                '80': 436, 
                                                '70': 397, 
                                                '60': 358, 
                                                '50': 322, 
                                                '40': 283, 
                                                '30': 244, 
                                                '20': 205, 
                                                '10': 166},
                                        '256':{ '100':1026,
                                                '90': 948,  
                                                '80': 870, 
                                                '70': 795, 
                                                '60': 717, 
                                                '50': 642, 
                                                '40': 564, 
                                                '30': 486, 
                                                '20': 411, 
                                                '10': 333}}}

Digital_xbar_area_dict = {'Digital_V1': { '32' : 0.16977,   # first indexed by version then by xbar_size
                                          '64' : 0.27701,
                                          '128': 1.74020,
                                          '256': 7.29481},
                          'Digital_V2': { '32' : 0.16949,  
                                          '64' : 0.27645,
                                          '128': 1.73908,
                                          '256': 7.29257}}

Digital_xbar_energy_dict = {'Digital_V1':{'32':{'100':5261.43744,  # first indexed by version then by xbar_size and then by % of non_0 values
                                                '90': 4613.872832, # For V1 it is (4n+2)*T and for V2 it is (3n+2+xbar_size)*T
                                                '80': 4128.199376, # in pJ
                                                '70': 3642.52592, 
                                                '60': 3156.852464, 
                                                '50': 2671.179008, 
                                                '40': 2023.6144, 
                                                '30': 1537.940944, 
                                                '20': 1052.267488, 
                                                '10': 566.594032},      
                                          '64':{'100':20844.00864, 
                                                '90': 18581.86252,
                                                '80': 16642.88014, 
                                                '70': 14380.73402, 
                                                '60': 12441.75163, 
                                                '50': 10502.76925, 
                                                '40': 8240.623131, 
                                                '30': 6301.640745, 
                                                '20': 4039.494628, 
                                                '10': 2100.512242},      
                                        '128':{'100': 83018.14464,
                                                '90': 74619.39346, 
                                                '80': 66220.64228, 
                                                '70': 57821.8911, 
                                                '60': 49423.13992, 
                                                '50': 41670.44653, 
                                                '40': 33271.69535, 
                                                '30': 24872.94417, 
                                                '20': 16474.19299, 
                                                '10': 8075.441812},     
                                        '256':{'100': 331639.0958, 
                                                '90': 298022.5268,
                                                '80': 264405.9578, 
                                                '70': 232082.3337, 
                                                '60': 198465.7647, 
                                                '50': 166142.1407, 
                                                '40': 132525.5717, 
                                                '30': 98909.00265, 
                                                '20': 66585.3786, 
                                                '10': 32968.80959}},
                            'Digital_V2':{'32':{'100':4466.744263,
                                                '90': 4053.765767,
                                                '80': 3744.031895, 
                                                '70': 3434.298023, 
                                                '60': 3124.564151, 
                                                '50': 2814.830279, 
                                                '40': 2401.851783, 
                                                '30': 2092.117911, 
                                                '20': 1782.384039, 
                                                '10': 1472.650167},  
                                          '64':{'100':17654.27322,
                                                '90': 16216.06481,  
                                                '80': 14983.31474, 
                                                '70': 13545.10633, 
                                                '60': 12312.35626, 
                                                '50': 11079.6062, 
                                                '40': 9641.397787, 
                                                '30': 8408.647721, 
                                                '20': 6970.439311, 
                                                '10': 5737.689245},
                                        '128':{'100': 70237.24474,
                                                '90': 64904.19392,  
                                                '80': 59571.14309, 
                                                '70': 54238.09226, 
                                                '60': 48905.04144, 
                                                '50': 43982.22529, 
                                                '40': 38649.17446, 
                                                '30': 33316.12363, 
                                                '20': 27983.07281, 
                                                '10': 22650.02198},
                                        '256':{'100': 280471.5471,
                                                '90': 259128.5,  
                                                '80': 237785.453, 
                                                '70': 217263.2925, 
                                                '60': 195920.2454, 
                                                '50': 175398.0849, 
                                                '40': 154055.0379, 
                                                '30': 132711.9909, 
                                                '20': 112189.8303, 
                                                '10': 90846.78326}}}
Digital_xbar_pow_leak_dict = {  '32' :5.575928889,          #in mW 
                                '64' :12.82466678,
                                '128':40.24037556,
                                '256':120.2098611}

# DAC - Discuss exact values with ISSAC authors
dac_lat_dict = {'1' : 1,
                '2' : 1,
                '4' : 1,
                '8' : 1,
                '16': 1}

dac_pow_dyn_dict = {'1' : 0.00350625,
                    '2' : 0.00350625,
                    '4' : 0.00350625,
                    '8' : 0.00350625,
                    '16': 0.00350625}

dac_pow_leak_dict = {'1' : 0.000390625,
                     '2' : 0.000390625,
                     '4' : 0.000390625,
                     '8' : 0.000390625,
                     '16': 0.000390625}

dac_area_dict = {'1' : 1.67 * 10**(-7),
                 '2' : 1.67 * 10**(-7),
                 '4' : 1.67 * 10**(-7),
                 '8' : 1.67 * 10**(-7),
                 '16': 1.67 * 10**(-7)}

# ADC - Discuss exact values with ISSAC authors
# ADC Values for including sparsity
adc_lat_dict = {'1' : 12.5,
                '2' : 25,
                '3' : 37.5,
                '4' : 50,
                '5' : 62.5,
                '6' : 75,
                '7' : 87.5,
                '8' : 100,
                '16': 200}

adc_pow_dyn_dict = {'1' : 0.225,
                    '2' : 0.45,
                    '3' : 0.675,
                    '4' : 0.9,
                    '5' : 1.125,
                    '6' : 1.35,
                    '7' : 1.575,
                    '8' : 1.8,
                    '16': 3.6}

adc_pow_leak_dict = {'1' : 0.025,
                     '2' : 0.05,
                     '3' : 0.075,
                     '4' : 0.1,
                     '5' : 0.125,
                     '6' : 0.15,
                     '7' : 0.175,
                     '8' : 0.2,
                     '16': 0.4}

adc_area_dict = {'1' : 0.0012,
                 '2' : 0.0012,
                 '3' : 0.0012,
                 '4' : 0.0012,
                 '5' : 0.0012,
                 '6' : 0.0012,
                 '7' : 0.0012,
                 '8' : 0.0012,
                 '16': 0.0012}

# SNH (MVM pipeline)
snh_lat = 1
snh_pow_leak = 9.7 * 10**(-7)
snh_pow_dyn = 9.7 * 10**(-6) - snh_pow_leak
snh_area = 0.00004 / 8 / 128

# SNA (MVM pipeline)
sna_lat = 1
sna_pow_leak = 0.005
sna_pow_dyn = 0.05 - sna_pow_leak
sna_area = 0.00006

# ALU (Part of Vector Functional Unit)
alu_lat = 1
alu_pow_dyn = 2.4 * 32/45
alu_pow_div_dyn = 1.52 * 32/45
alu_pow_mul_dyn = 0.795 * 32/45
alu_pow_others_dyn = 0.373 * 32/45 # logical, eq, relu, add, sub, lsh, rsh
alu_pow_leak = 0.27 * 32/45
alu_area = 0.00567 * 32/45

# witout considering division
#alu_lat = 1
#alu_pow_dyn = 1.15 * 32/45
#alu_pow_mul_dyn = 0.796 * 32/45
#alu_pow_others_dyn = 0.36 * 32/45 # logical, eq, relu, add, sub, lsh, rsh
#alu_pow_leak = 0.05 * 32/45
#alu_area = 0.002326 * 32/45

# Sigmoid/Tanh (Part of Vector Functional Unit) - Taken from ISAAC paper
act_lat = 1 # added for 4 exponential units
act_pow_leak = 0.026
act_pow_dyn = 0.26 - act_pow_leak
act_area = 0.0003 # check this ???

# Multiplexer - These should be analog muxes
mux_lat = 0
mux_pow_leak = 0
mux_pow_dyn = 0
mux_area = 0

# Data Memory value dictionary
dataMem_lat_dict = {'256' : 1,
                    '512' : 1,
                    '1024': 1,
                    '2048': 1}

dataMem_pow_dyn_dict = {'256' : 0.16,
                        '512' : 0.24,
                        '1024': 0.33,
                        '2048': 0.57}

dataMem_pow_leak_dict = {'256' : 0.044,
                         '512' : 0.078,
                         '1024': 0.147,
                         '2048': 0.33}

dataMem_area_dict = {'256' : 0.00056,
                     '512' : 0.00108,
                     '1024': 0.00192,
                     '2048': 0.00392}

dataMem_lat_dict = {'256' : 1,
                    '512' : 1,
                    '1024': 1,
                    '2048': 1}

dataMem_pow_dyn_dict = {'256' : 0.16,
                        '512' : 0.24,
                        '1024': 0.33,
                        '2048': 0.57}

dataMem_pow_leak_dict = {'256' : 0.044,
                         '512' : 0.078,
                         '1024': 0.147,
                         '2048': 0.33}

dataMem_area_dict = {'256' : 0.00056,
                     '512' : 0.00108,
                     '1024': 0.00192,
                     '2048': 0.00392}

# Instruction Memory value dictionary
instrnMem_lat_dict = {'512' : 1,
                      '1024': 1,
                      '2048': 1}

instrnMem_pow_dyn_dict = {'512' : 0.46,
                          '1024': 0.53,
                          '2048': 0.65}

instrnMem_pow_leak_dict = {'512' : 0.078,
                           '1024': 0.147,
                           '2048': 0.33}

instrnMem_area_dict = {'512' : 0.00108,
                       '1024': 0.00192,
                       '2048': 0.0041}

# Xbar_inMem value dictionary (1 access means reading (dac_res) bits for each xbar row)
# for computing average power of ima - scale dyn_pow down by xbar_size
xbar_inMem_lat_dict = {'32'  : 1, # indexed with xbar size
                       '64'  : 1,
                       '128' : 1,
                       '256' : 1}

xbar_inMem_pow_dyn_read_dict = {'32'  : 0.3,
                                '64'  : 0.7,
                                '128' : 1.7,
                                '256' : 4.7}

xbar_inMem_pow_dyn_write_dict = {'32'  : 0.1,
                                 '64'  : 0.1,
                                 '128' : 0.16,
                                 '256' : 0.2}

xbar_inMem_pow_leak_dict = {'32'  : 0.009,
                            '64'  : 0.02,
                            '128' : 0.04,
                            '256' : 0.075}

xbar_inMem_area_dict = {'32'  : 0.00015,
                        '64'  : 0.00033,
                        '128' : 0.00078,
                        '256' : 0.0019}

# Xbar_outMem value dictionary
xbar_outMem_lat_dict = {'32'  : 1, # indexed with xbar size
                       '64'   : 1,
                       '128'  : 1,
                       '256'  : 1}

xbar_outMem_pow_dyn_dict = {'32'  : 0.1,
                           '64'   : 0.1,
                           '128'  : 0.16,
                           '256'  : 0.2}

xbar_outMem_pow_leak_dict = {'32'  : 0.009,
                            '64'   : 0.02,
                            '128'  : 0.04,
                            '256'  : 0.075}

xbar_outMem_area_dict = {'32'  : 0.00015,
                        '64'   : 0.00033,
                        '128'  : 0.00078,
                        '256'  : 0.0019}


# Chosen latency based on config file - only for components whose latency is parameter dependent
#xbar_lat = xbar_lat_dict [str(cfg.xbar_bits)][str(cfg.xbar_size)]
# xbar_innerp_lat_dict = {'32':{'100':0, '90':0, '80':0, '70':0, '60':0, '70':0, '50':0, '40':0, '30':0, '20':0, '10':0},
#                         '64':{'100':0, '90':0, '80':0, '70':0, '60':0, '70':0, '50':0, '40':0, '30':0, '20':0, '10':0},
#                         '128':{'100':0, '90':0, '80':0, '70':0, '60':0, '70':0, '50':0, '40':0, '30':0, '20':0, '10':0},
#                         '256':{'100':0, '90':0, '80':0, '70':0, '60':0, '70':0, '50':0, '40':0, '30':0, '20':0, '10':0}}
xbar_ip_lat_dict = {'100':0, '90':0, '80':0, '70':0, '60':0, '70':0, '50':0, '40':0, '30':0, '20':0, '10':0}
if cfg.MVMU_ver == "Analog":
      for key, value in xbar_ip_lat_dict.items():
            xbar_ip_lat_dict[key] = xbar_ip_lat
else:
      xbar_ip_lat_dict = Digital_xbar_lat_dict[cfg.MVMU_ver][str(cfg.xbar_size)]
print("xbar_ip_lat_dict",xbar_ip_lat_dict)


xbar_op_lat = xbar_op_lat
xbar_rd_lat = xbar_rd_lat
xbar_wr_lat = xbar_wr_lat
dac_lat = dac_lat_dict [str(cfg.dac_res)]
#FIXME need to review it I can remove adc_lat property
adc_lat = adc_lat_dict [str(cfg.adc_res)]
xbar_inMem_lat = xbar_inMem_lat_dict[str(cfg.xbar_size)]
xbar_outMem_lat = xbar_outMem_lat_dict[str(cfg.xbar_size)]
instrnMem_lat =  instrnMem_lat_dict[str(cfg.instrnMem_size)]
dataMem_lat =  dataMem_lat_dict[str(cfg.dataMem_size)]

# Chosen area based on config file - only for components whose latency is parameter dependent
if cfg.MVMU_ver == "Analog":
        xbar_area = xbar_area_dict[str(cfg.xbar_bits)][str(cfg.xbar_size)]
else:
        xbar_area = Digital_xbar_area_dict[cfg.MVMU_ver][str(cfg.xbar_size)]
dac_area = dac_area_dict [str(cfg.dac_res)]
adc_area = adc_area_dict [str(cfg.adc_res)]
xbar_inMem_area = xbar_inMem_area_dict[str(cfg.xbar_size)]
xbar_outMem_area = xbar_outMem_area_dict[str(cfg.xbar_size)]
instrnMem_area =  instrnMem_area_dict[str(cfg.instrnMem_size)] * math.sqrt(8) #area scaling for 8 bytes per instruction
dataMem_area =  dataMem_area_dict[str(cfg.dataMem_size)]

# Chosen dyn_power based on config file - only for components whose latency is parameter dependent
#xbar_pow_dyn = xbar_pow_dict [str(cfg.xbar_bits)][str(cfg.xbar_size)]
xbar_ip_pow_dyn = xbar_ip_pow
xbar_op_pow_dyn = xbar_op_pow
xbar_rd_pow_dyn = xbar_rd_pow
xbar_wr_pow_dyn = xbar_wr_pow
dac_pow_dyn = dac_pow_dyn_dict [str(cfg.dac_res)]
adc_pow_dyn = adc_pow_dyn_dict [str(cfg.adc_res)]
xbar_inMem_pow_dyn_read = xbar_inMem_pow_dyn_read_dict[str(cfg.xbar_size)]
xbar_inMem_pow_dyn_write = xbar_inMem_pow_dyn_write_dict[str(cfg.xbar_size)]
xbar_outMem_pow_dyn = xbar_outMem_pow_dyn_dict[str(cfg.xbar_size)]
instrnMem_pow_dyn =  instrnMem_pow_dyn_dict[str(cfg.instrnMem_size)] * math.sqrt(8) #area scaling for 8 bytes per instruction
dataMem_pow_dyn =  dataMem_pow_dyn_dict[str(cfg.dataMem_size)]

# Energy
xbar_ip_energy_dict = {'100':0, '90':0, '80':0, '70':0, '60':0, '70':0, '50':0, '40':0, '30':0, '20':0, '10':0}
if cfg.MVMU_ver == "Analog":
        for key,value in xbar_ip_energy_dict.items():
                xbar_ip_energy_dict[key] = xbar_ip_lat*xbar_ip_pow_dyn
else:
        xbar_ip_energy_dict = Digital_xbar_energy_dict[cfg.MVMU_ver][str(cfg.xbar_size)]
print('xbar_ip_energy_dict', xbar_ip_energy_dict)

# Chosen leak_power based on config file - only for components whose latency is parameter dependent
if cfg.MVMU_ver == "Analog":
        xbar_pow_leak = 0
else:
        xbar_pow_leak = Digital_xbar_pow_leak_dict[str(cfg.xbar_size)]
dac_pow_leak = dac_pow_leak_dict [str(cfg.dac_res)]
adc_pow_leak = adc_pow_leak_dict [str(cfg.adc_res)]
xbar_inMem_pow_leak = xbar_inMem_pow_leak_dict[str(cfg.xbar_size)]
xbar_outMem_pow_leak = xbar_outMem_pow_leak_dict[str(cfg.xbar_size)]
instrnMem_pow_leak =  instrnMem_pow_leak_dict[str(cfg.instrnMem_size)] * math.sqrt(8) #area scaling for 8 bytes per instruction
dataMem_pow_leak =  dataMem_pow_leak_dict[str(cfg.dataMem_size)]

# Core Control unit (control unit and pipeline registers)
ccu_pow = 1.25*0.2 #0.2 for activvity
ccu_area = 0.00145*2.25 #taken similar as edctrl (scaled by power)

# Added here for simplicity now (***can need modification later***)
# The latency of mem access is dependent on when can the ima find edram bys non-busy
memInterface_lat = infinity # infinite latency

#############################################################################################################
# Tile Hierarchy
    # Number of IMAs
    # EDRAM size
    # Shared Bus width
    # Instruction memory size
    # Receive Buffer size
#############################################################################################################

# Tile component latency/pow/area
# EDRAM value dictionary (counter storage is not coounted)
edram_lat_dict = {'8'  :2,
                  '64' : 2, #edram access width is constant = 256 bits
                  '128': 2}

edram_pow_dyn_dict = {'8' : 17.2/2,
                      '64' : 17.2/2, # (0.0172 nJ with 2 cycles access latency)
                      '128': 25.35/2}

edram_pow_leak_dict = {'8' : 0.46,
                       '64' : 0.46,
                       '128': 0.77}

edram_area_dict = {'8' : 0.086,
                   '64' : 0.086,
                   '128': 0.121}

# Tile Instruction Memory value dictionary
tile_instrnMem_lat_dict = {'512' : 1,
                          '1024': 1,
                          '2048': 1}

tile_instrnMem_pow_dyn_dict = {'512' : 0.46,
                               '1024': 0.53,
                               '2048': 0.65}

tile_instrnMem_pow_leak_dict = {'512' : 0.078,
                                '1024': 0.147,
                                '2048': 0.33}

tile_instrnMem_area_dict = {'512' : 0.00108,
                            '1024': 0.00192,
                            '2048': 0.0041}

# counter storage (2048 Byte Scratch RAM - 1 counter entry shared by 256 bits of data (16 neurons))
# area scaling (X8)
counter_buff_lat = 1 * math.sqrt(8)
counter_buff_pow_dyn = 0.65/2 * math.sqrt(8)
counter_buff_pow_leak = 0.33/2 * math.sqrt(8)
counter_buff_area = 0.0041 * math.sqrt(8)

# EDRAM to IMA bus values
edram_bus_lat = 1
edram_bus_pow_dyn = 6/2 #bus width = 384, same as issac (over two cycles)
edram_bus_pow_leak = 1/2 #bus width = 384, same as issac
edram_bus_area = 0.090

# EDRAM controller values
edram_ctrl_lat = 1
edram_ctrl_pow_dyn = 0.475
edram_ctrl_pow_leak = 0.05
edram_ctrl_area = 0.00145

# Receive buffer value dictionary - 16 entries (Need to make this a dictionary)
# Increasing to 64 entries
receive_buffer_lat = 1 * math.sqrt(4)
receive_buffer_pow_dyn = 4.48 * math.sqrt(4) # (0.2*256/16)
receive_buffer_pow_leak = 0.09 * math.sqrt(4)
receive_buffer_area = 0.0022 *math.sqrt(4)


# Chosen latency based on config file - only for components whose latency is parameter dependent
edram_lat = edram_lat_dict[str(cfg.edram_size)]
tile_instrnMem_lat = tile_instrnMem_lat_dict[str(cfg.tile_instrnMem_size)]

# Chosen area based on config file - only for components whose area is parameter dependent
edram_area = edram_area_dict[str(cfg.edram_size)]
tile_instrnMem_area = tile_instrnMem_area_dict[str(cfg.tile_instrnMem_size)] * math.sqrt(8) #area scaling for 8 bytes per instruction

# Chosen dynamic power based on config file - only for components whose dynamic power is parameter dependent
edram_pow_dyn = edram_pow_dyn_dict[str(cfg.edram_size)]
tile_instrnMem_pow_dyn = tile_instrnMem_pow_dyn_dict[str(cfg.tile_instrnMem_size)] * math.sqrt(8) #area scaling for 8 bytes per instruction

# Chosen leakage power based on config file - only for components whose leakage power is parameter dependent
edram_pow_leak = edram_pow_leak_dict[str(cfg.edram_size)]
tile_instrnMem_pow_leak = tile_instrnMem_pow_leak_dict[str(cfg.tile_instrnMem_size)] * math.sqrt(8) #area scaling for 8 bytes per instruction

# Tile Control unit
tcu_pow = 0.25*0.2
tcu_area = 0.00145 #taken similar as edctrl

#############################################################################################################
# Node Hierarchy
    # Number of Tiles
    # NOC - Topology (Currently assumes a cmesh (c=4, same as ISSAC))
        # n = number of dimension\
        # k = number of tiles in each dimension
        # c = concentartion (tiles/router)
        # average injection rate (0.25 - a tile injects a new packet for each destination in every four cycles)
#############################################################################################################

# NOC latency dictionary (in terms of flit cycle)
# Note - if inj_rate (packet injection -1 packet - 16 neurons) exceeds 0.025 - there's a problem, NoC needs to be redesigned else network latency will be killing!
# Hence, not provided for
noc_inj_rate_max = 0.025
noc_lat_dict = {'0.001': 29,
                '0.005': 31,
                '0.01' : 34,
                '0.02' : 54,
                '0.025': 115}

noc_area_dict = {'4': 0.047,
                 '8': 0.116}

# Router dynamic power - NOC will be used only if atleast oen of send_queue in node is non_empty
noc_pow_dyn_dict = {'4': 16.13,
                      '8': 51.48}

# Router leakage power - NOC will be used only if atleast oen of send_queue in node is non_empty
noc_pow_leak_dict = {'4': 0.41,
                       '8': 1.04}

# Enter component latency (Based on teh above NOC topological parameters)
# Inter-node Noc (router & channel)
assert (cfg.noc_inj_rate <= noc_inj_rate_max), 'Oops: reconsider NOC design and or DNN mapping, with this inj_rate, NOC data transfer throughput \
will be terrible!'

noc_intra_lat = noc_lat_dict[str(cfg.noc_inj_rate)]
noc_intra_pow_dyn = noc_pow_dyn_dict[str(cfg.noc_num_port)] # per router
noc_intra_pow_leak = noc_pow_leak_dict[str(cfg.noc_num_port)]# per router
noc_intra_area = noc_area_dict[str(cfg.noc_num_port)] # per router

# Hypertransport network (HT)
# Note HT is external to a node, but we consider all tiles in one
# virtual node itself for simplicity
# HT numbers from ISAAC = 6.4GB/s = 6.4B/ ns = 1packet(16*2 Bytes) = 5ns
ht_lat = 5 #latency per packet
noc_inter_lat = ht_lat + noc_intra_lat #navigate to the node, then to tile within node
noc_inter_pow_dyn = 10400 #10.4W
noc_inter_pow_leak = 0
noc_inter_area = 22.88

