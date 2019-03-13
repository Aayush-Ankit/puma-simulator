# APIs to compute tile power and area stats
import sys

# import dependency files
import config as cfg
import constants as param
import ima_metrics

# Compute metrics of the tile based on paramaters in config file and dicts file constants file
# Area is computed as the summation of all component area (doesn't consider physical layout)
def compute_area (): #in mm2
    area = 0.0
    area += cfg.num_ima * ima_metrics.compute_area ()
    area += param.counter_buff_area
    area += param.edram_bus_area
    area += param.edram_ctrl_area
    area += param.receive_buffer_area
    area += param.tile_instrnMem_area
    area += param.edram_area
    area += param.tcu_area
    #print ('Tile area: ' + str (area) + ' mm2')

    #tile_issac_area = 0.20668 + 0.090 + 0.083 + 0.0006 + 0.00006 + \
    #        0.00024 + 0.0032 # Taken from issac paper (except router area)
    #print (tile_issac_area)
    #print ('Tile Area inrease for iso xbars: ' + str (((area - tile_issac_area)/tile_issac_area)*100) + ' %')
    return area

# Leakage power is computed as sum of leakage powers of all components
def compute_pow_leak ():
    leak_pow = 0.0
    leak_pow += cfg.num_ima * ima_metrics.compute_pow_leak ()
    leak_pow += param.counter_buff_pow_leak
    leak_pow += param.edram_bus_pow_leak
    leak_pow += param.edram_ctrl_pow_leak
    leak_pow += param.receive_buffer_pow_leak
    leak_pow += param.tile_instrnMem_pow_leak
    leak_pow += param.edram_pow_leak
    #print ('Tile leak power: ' + str (leak_pow) + ' mW')
    return leak_pow

# useful in computing tile leakage for ima-power-gating
def compute_pow_leak_non_ima ():
    leak_pow = 0.0
    leak_pow += param.counter_buff_pow_leak
    leak_pow += param.edram_bus_pow_leak
    leak_pow += param.edram_ctrl_pow_leak
    leak_pow += param.receive_buffer_pow_leak
    leak_pow += param.tile_instrnMem_pow_leak
    leak_pow += param.edram_pow_leak
    #print ('Tile leak power: ' + str (leak_pow) + ' mW')
    return leak_pow

# Peak dynakic power (assumes all components are being accessed in each cycle)
def compute_pow_dyn ():
    dyn_pow = 0.0
    dyn_pow += cfg.num_ima * ima_metrics.compute_pow_dyn ()
    dyn_pow += param.counter_buff_pow_dyn
    dyn_pow += param.edram_bus_pow_dyn
    dyn_pow += param.edram_ctrl_pow_dyn
    dyn_pow += param.receive_buffer_pow_dyn
    dyn_pow += param.tile_instrnMem_pow_dyn
    dyn_pow += param.edram_pow_dyn
    #print ('Tile peak dynmaic power: ' + str (dyn_pow) + ' mW')
    return dyn_pow

# Peak power of tile - leak_pow + peak dyn_pow
def compute_pow_peak ():
    peak_pow = compute_pow_leak() + compute_pow_dyn() # 6 IMA
    #print ('Tile peak (leak+dyn) power: ' + str (peak_pow) + ' mW')

    ## Compare with ISSAC for iso-xbars (computational effciiency - ops/mm2)
    #issac_tile_pow = 289 + 20.7 + 7 + 0.52 + 0.05 + 0.4 + 1.68
    #print ('Peak power increase for iso xbars: ' + str((peak_pow - issac_tile_pow) / (issac_tile_pow)*100) + ' %')
    return peak_pow

#compute_area ()
#compute_pow_leak ()
#compute_pow_dyn ()
#compute_pow_peak ()
