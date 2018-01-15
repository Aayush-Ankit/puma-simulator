import math
import sys
sys.path.insert (0, '/home/aa/dpe_emulate/include')
import matplotlib.pyplot as plt
from collections import OrderedDict

import config as cfg
# PUMA tile sweep (parameters) for CE(computation efficiency)
# PE is measured as the number of 16-bit operations performed per second per W

# Computation units:
# 1. xbar for matrix-vector multiplication
# 2. vfu for performing vector operations
# 3. rom (dataMem embedded ROM-RAM) for look-up table based operations

# datamemory (4*xbar_size*(num_xbar/8)) - Constant (from PUMA compiler based on register allocation)

# Time step considered (based on xbar latency) = 128ns

# Sweep Parameters considered:
xbar_size_list = [64, 128, 256]
num_xbar_list = [8, 16, 32] # [xbar_size (DACs,SnH), 1 ADC, 1 SnA per xbar]
num_vfu_list = [1, 8, 64]
num_core_list = [4, 8, 16, 32]

#xbar_size_list = [128, 256]
#num_xbar_list = [16] # [xbar_size (DACs,SnH), 1 ADC, 1 SnA per xbar]
#num_vfu_list = [1]
#num_core_list = [8]

time_step_dict = {'64':60, '128':100, '256':230}

num_data_points = len(xbar_size_list) * len(num_xbar_list) * len(num_vfu_list) * len(num_core_list)
print ('num_data_points', num_data_points)

ns = 10**(-9) #wrt seconds
mw = 10**(-3) #wrt watt
mm2 = 1 #wrt millimetres2
# Logical to physical xbar ratio
log2phy_xbfactor = cfg.data_width / cfg.xbar_bits # logical xbar count
# xbar latency for 128 sized xbar in ns
time_step = 100

# fixing the number of ADCs in a core
num_adc = 16


# Component power in mW (per component)
xbar128_pow = 0.3
dac_pow = 0.0039
adc_pow = 2
snh_pow = 9.7 *(10**(-6) + 10**(-7))
sna_pow = 0.055
alu_pow =  2.67 * 32/45
dataMem128_2_pow = 0.477
instrnMem_pow = 0.538 * math.sqrt(8)
xbar_inMem128_pow = 0.97 #dyn is average of read and write
xbar_outMem128_pow = 0.20
ccu_pow = 1.25*0.2

edram_pow = 17.66 # (for 1 cyc latency)
tile_instrnMem_pow = 0.677 * math.sqrt(8) #1024 entries
counter_buff_pow = 0.98 * math.sqrt(8) # (for 1 cyc latency)
edram_bus_pow = 0.7 # (for 1 cyc latency)
edram_ctrl_pow = 0.525
receive_buffer_pow = 4.57 * math.sqrt(4)
tcu_pow = 0.25*2
router_pow = 16.54/cfg.cmesh_c

# Function to measure tile are for given parameters # in mm2
def get_tile_power (xbar_size, num_xbar, num_vfu, num_core):
    core_power = 0.0
    # assumption xbar power scales quadratically with xbar_size (Confirm with JPS)
    core_power += num_xbar * ((xbar_size/128.0)**2) * xbar128_pow

    core_power += num_xbar/log2phy_xbfactor * xbar_size * dac_pow
    # adc power is dependent on xbar_size - some components have exponential dependance
    core_power += num_xbar * adc_pow * (xbar_size/128.0)**(2.3)
    core_power += num_xbar * xbar_size * snh_pow
    core_power += num_xbar * sna_pow
    core_power += num_vfu * alu_pow
    # memory units grow as square root w.r.t. number of entries
    core_power += math.sqrt((xbar_size/128.0) * (num_xbar/16.0)) * dataMem128_2_pow
    # instrn mem power (size) is dependent on num_xbars (num_mvms a core can do)
    # memory units grow as square root w.r.t. number of entries
    core_power += math.sqrt(num_xbar/16.0) * instrnMem_pow
    # memory units grow as square root w.r.t. number of entries
    core_power += math.sqrt(xbar_size/128.0) * (num_xbar/8.0) * xbar_inMem128_pow
    # memory units grow as square root w.r.t. number of entries
    core_power += math.sqrt(xbar_size/128.0) * (num_xbar/8.0) * xbar_outMem128_pow
    core_power += ccu_pow
    tile_power = num_core * core_power
    #tile_power += math.sqrt((num_core/8.0)*(xbar_size/128.0)*(num_xbar/16.0)) * edram_power
    tile_power += math.sqrt(num_core/8.0) * edram_pow
    # Less send and receives between tiles
    tile_power += tile_instrnMem_pow / (math.sqrt((xbar_size/128.0)*(num_xbar/16.0)))
    tile_power += math.sqrt((xbar_size/128.0)*(num_xbar/16.0)) * counter_buff_pow
    tile_power += num_core/8.0 * edram_bus_pow
    tile_power += num_core/8.0 * edram_ctrl_pow
    # Less tiles will fan-out to a next layer tile
    # Less send and receives between tiles
    tile_power += receive_buffer_pow/ (math.sqrt((xbar_size/128.0)*(num_xbar/16.0)))
    tile_power += tcu_pow
    tile_power += router_pow
    return (tile_power * mw) #in W


# Measure the number of computations for given parameters
def get_num_comp (xbar_size, num_xbar, num_vfu, num_core):
    num_comp_xbar = num_xbar/log2phy_xbfactor * (xbar_size*xbar_size) / math.ceil(xbar_size/128.0)
    num_comp_vfu = xbar_size * num_vfu
    num_comp_rom = xbar_size # lut (1 RAM read, 1 ROM read, 1 RAM write, 1 ALU for interpolation)
    num_comp_total = num_core*(num_comp_xbar + num_comp_vfu + num_comp_rom)
    return num_comp_total


def get_time (xbar_size, num_xbar, num_vfu, num_core):
    # assumption: xbar latency scales linearly with xbar_size (Confirm with John-Paul)
    # A highly parallel synthtic workload going through all units (VFU, MVM, MEU) in Core
    # all xbars in a core share data
    # all xbars in a core run in ||el
    # all xbars outputs go through vfu (to get xbar_size outputs)
    # all vfu outputs go through lut
    # xbar_size outputs are stored
    # overall time makes sure that last core's store finishes
    #time_step_new = time_step * (xbar_size/128.0)
    time_step_new = time_step_dict[str(xbar_size)]
    ld_time = num_core * (xbar_size/16.0) #1 edram read is 16 entries 1ns
    mvm_time = (16+1) * time_step_new * math.ceil((num_xbar/float(num_adc)))
    vfu_time = time_step_new * math.ceil((num_xbar/8.0)/num_vfu)
    #vfu_time = 0
    lut_time = time_step_new
    #lut_time = 0
    st_time = xbar_size/16.0
    time_total = ld_time + mvm_time + vfu_time + lut_time + st_time
    return time_total * ns


# Sweep to generate computational efficiency data
#ce_dict = OrderedDict()
pe_list = []
name_list = []
for xbar_size in xbar_size_list:
    if (xbar_size != xbar_size_list[0]):
        # Add space between bars
        pe_list.append(0)
        name_list.append(' ')
        pe_list.append(0)
        name_list.append(' ')
        pe_list.append(0)
        name_list.append(' ')
    for num_vfu in num_vfu_list:
        # Add space between bars
        pe_list.append(0)
        name_list.append(' ')
        pe_list.append(0)
        name_list.append(' ')
        for num_xbar in num_xbar_list:
            # Add space between bars
            pe_list.append(0)
            name_list.append(' ')
            for num_core in num_core_list:
                #tile_energy = get_tile_energy (xbar_size, num_xbar, num_vfu, num_core)
                tile_power = get_tile_power (xbar_size, num_xbar, num_vfu, num_core)
                #print ('tile_power', tile_power)
                num_comp_total = get_num_comp (xbar_size, num_xbar, num_vfu, num_core)
                #print ('num_comp_total', num_comp_total)
                #time = get_time (xbar_size, num_xbar, num_vfu, num_core)
                #pe = num_comp_total / (tile_energy / time) #inGops/Watt
                pe = num_comp_total/ tile_power / (10**3) #inGops/Watt
                name = 'S'+str(xbar_size)+'-V'+str(num_vfu)+'-X'+str(num_xbar)+'-C'+str(num_core)
                #ce_dict[name] = ce
                pe_list.append(pe)
                name_list.append(name)

# Plot the sweep
#plt.bar(range(len(ce_dict)), ce_dict.values(), align='center')
#plt.xticks(range(len(ce_dict)), ce_dict.keys())

pe_list1 = [x/2 for x in pe_list]
plt.bar(range(len(pe_list)), pe_list1, align='center')
plt.xticks(range(len(name_list)), name_list)

plt.xticks(fontsize=6, rotation=70)
#plt.autoscale(tight=True)
plt.show()
#plt.savefig('/home/aa/dpe_emulate/isca_results/puma_ce_sweep')



