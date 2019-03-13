# APIs to compute tile power and area stats
import sys

import numpy as np

# import dependency files
import config as cfg
import constants as param
import ima_metrics
import tile_metrics

# Compute metrics of the node based on parameetrs in configuration file and dicts in constants file
# Area is computed as the summation of all component area (doesn't consider physical layout)
def compute_area (): #in mm2
    area = 0.0
    #area += cfg.num_tile_compute * tile_metrics.compute_area ()
    #area += param.noc_intra_area * (cfg.num_node*(cfg.num_tile_compute+2)) / float(cfg.cmesh_c)
    # Area of all tiles on chip
    area += cfg.num_tile_max * tile_metrics.compute_area ()
    area += param.noc_intra_area * (cfg.num_node*(cfg.num_tile_max)) / float(cfg.cmesh_c)
    area += param.noc_inter_area
    #print ('Node area excludes NOC: ', area)
    return area

# Leakage power is computed as sum of leakage powers of all components
def compute_pow_leak ():
    leak_pow = 0.0
    leak_pow += cfg.num_tile_compute * tile_metrics.compute_pow_leak ()
    leak_pow += param.noc_intra_pow_leak * (cfg.num_node*cfg.num_tile_compute) / float(cfg.cmesh_c)
    #print ('Node leakage power excludes NOC: ', leak_pow)
    return leak_pow

# Peak dynamic power (assumes all components are being accessed in each cycle)
def compute_pow_dyn ():
    dyn_pow = 0.0
    dyn_pow += cfg.num_tile_compute * tile_metrics.compute_pow_dyn ()
    dyn_pow += param.noc_intra_pow_dyn * (cfg.num_node*cfg.num_tile_compute) / float(cfg.cmesh_c)
    #print ('Node peak dynamic power excludes NOC: ', dyn_pow)
    return dyn_pow

# Peak power of node - leak_pow + peak dyn_pow
def compute_pow_peak ():
    peak_pow = compute_pow_leak() + compute_pow_dyn() # 6 IMA
    #print ('Node peak power excludes NOC: ', peak_pow)
    return peak_pow

#compute_area ()
#compute_pow_leak ()
#compute_pow_dyn ()
#compute_pow_peak ()
