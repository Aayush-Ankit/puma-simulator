# Top module name
set TOP edram_controller
#set TOP qcc
# verilog source files
set sverilog_files [list edram_controller.sv]
#set verilog_files [list Ann_ver.v mActFn.v mDotProduct.v SelectShiftAddv6.v controlSigNew.v AlphabetSet.v]
#set verilog_files [list qcc.v oneddct_orig.sv oneddct_approx.sv]
#set verilog_files [list "qcc_syn_flat_before_gtech.sv"]
# timing constaints for pure combinational logic
#set my_max_delay 1

# clock period (ns): timing constraints
set my_period_ns  1

# clock uncertainty (ns)
set my_clock_uncertainty 0.1

# clock pin name
set clk_name clk


# You do not have to change from here.
# set target library
set target_library /package/cae3/mosispdk/ARMLIBS/IBM/IBM12SOI/sc12_base_v31_hvt/2009q2v1/db/sc12_base_v31_hvt_soi12s0_ff_nominal_min_0p99v_m40c_mns.db
set link_library { * /package/cae3/mosispdk/ARMLIBS/IBM/IBM12SOI/sc12_base_v31_hvt/2009q2v1/db/sc12_base_v31_hvt_soi12s0_ff_nominal_min_0p99v_m40c_mns.db }
set symbol_library /package/cae3/mosispdk/ARMLIBS/IBM/IBM12SOI/sc12_base_v31_hvt/2009q2v1/sdb/sc12_base_v31_hvt_soi12s0.sdb

#set target_library /package/cae3/mosispdk/ARMLIBS/IBM/IBM10SF/aci/sc-adv12/synopsys/scadv12_cmos10sf_rvt_ff_1p1v_125c.db
set synthetic_library /package/eda/synopsys/syn-I-2013.12-SP5-9/libraries/syn/dw_foundation.sldb
#set synthetic_library /package/eda/synopsys/syn-D-2010.03-SP3/libraries/syn/dw_foundation.sldb
#set link_library [concat "*" $target_library $synthetic_library]

# file name for synthesized verilog file
set synthesized_verilog_file ${TOP}_syn.sv
set flattened_verilog_file ${TOP}_syn_flat.sv

# read RTL files
analyze -f sverilog $sverilog_files

# elaborate
elaborate  $TOP
current_design $TOP

link
uniquify

# set timing constraints for combinational logic
#set_max_delay ${my_max_delay} -to [all_outputs]

# create clock
create_clock -period $my_period_ns $clk_name
set_clock_uncertainty $my_clock_uncertainty [get_clocks $clk_name]
# set_switching_activity -toggle_rate 0.5 -base_clock clk -static_probability 0.5 [all_inputs]

# enable power calculation
#saif_map -start
#set_power_prediction
#set_dont_touch [sub_designs_of $TOP]

#compile -map_effort high  -boundary_optimization
compile -map_effort high
#compile_ultra
#compile_ultra -no_autoungroup
#compile_ultra -no_boundary_optimization
#compile_ultra -incremental

#compile_ultra_ungroup_small_hierarchies false

check_design -summary
#> $LOG_PATH$TOPLEVEL-check_design.log


# netlist with hierarchy
write -f verilog -hierarchy -o $synthesized_verilog_file

# flattened netlist
#ungroup -all -flatten
#write -f verilog -o $flattened_verilog_file

# for combinational logic
# write_saif  -output ./${TOP}_switching.saif -propagated
report_timing > ./${TOP}_timing_${my_period_ns}ns.txt
report_area > ./${TOP}_area_${my_period_ns}ns.txt
report_power -hier > ./${TOP}_power_${my_period_ns}ns.txt

#report_timing
#report_area

#read_saif -input ann_saif -instance_name mAnnTb/iAnn
#report_power -hier

#report_power -hier -hier_level 3 > ./${TOP}_power_${my_max_delay}ns.txt

# write_sdc ./${TOP}_${my_max_delay}ns.sdc

quit

