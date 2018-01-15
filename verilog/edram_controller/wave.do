onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -expand -group ecif :edram_controller_test:ecif:ima_ren
add wave -noupdate -expand -group ecif :edram_controller_test:ecif:ima_wen
add wave -noupdate -expand -group ecif :edram_controller_test:ecif:ima_wait
add wave -noupdate -expand -group ecif -radix decimal :edram_controller_test:ecif:ima_addr
add wave -noupdate -expand -group ecif -radix decimal :edram_controller_test:ecif:ima_data
add wave -noupdate -expand -group ecif :edram_controller_test:ecif:ram_ren
add wave -noupdate -expand -group ecif :edram_controller_test:ecif:ram_wen
add wave -noupdate -expand -group ecif -radix decimal :edram_controller_test:ecif:ram_addr
add wave -noupdate -expand -group ecif -radix decimal :edram_controller_test:ecif:ram_data
add wave -noupdate -divider <NULL>
add wave -noupdate -expand -group DUT :edram_controller_test:DUT:clk
add wave -noupdate -expand -group DUT :edram_controller_test:DUT:nrst
add wave -noupdate -expand -group DUT :edram_controller_test:DUT:validfile
add wave -noupdate -expand -group DUT :edram_controller_test:DUT:state
add wave -noupdate -expand -group DUT -radix decimal :edram_controller_test:DUT:counter
add wave -noupdate -expand -group DUT -radix decimal :edram_controller_test:DUT:last_idx
add wave -noupdate -expand -group DUT :edram_controller_test:DUT:ren_rel
add wave -noupdate -expand -group DUT :edram_controller_test:DUT:wen_rel
add wave -noupdate -expand -group DUT -radix decimal :edram_controller_test:DUT:addr_rel
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {390 ns} 0}
quietly wave cursor active 1
configure wave -namecolwidth 293
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ns
update
WaveRestoreZoom {314 ns} {413 ns}
