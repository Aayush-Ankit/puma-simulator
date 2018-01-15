onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -expand -group dut :receive_buff_test:DUT:clk
add wave -noupdate -expand -group dut :receive_buff_test:DUT:nrst
add wave -noupdate -expand -group dut -radix decimal -childformat {{{:receive_buff_test:DUT:datafile[7]} -radix decimal} {{:receive_buff_test:DUT:datafile[6]} -radix decimal} {{:receive_buff_test:DUT:datafile[5]} -radix decimal} {{:receive_buff_test:DUT:datafile[4]} -radix decimal} {{:receive_buff_test:DUT:datafile[3]} -radix decimal} {{:receive_buff_test:DUT:datafile[2]} -radix decimal} {{:receive_buff_test:DUT:datafile[1]} -radix decimal} {{:receive_buff_test:DUT:datafile[0]} -radix decimal}} -subitemconfig {{:receive_buff_test:DUT:datafile[7]} {-radix decimal} {:receive_buff_test:DUT:datafile[6]} {-radix decimal} {:receive_buff_test:DUT:datafile[5]} {-radix decimal} {:receive_buff_test:DUT:datafile[4]} {-radix decimal} {:receive_buff_test:DUT:datafile[3]} {-radix decimal} {:receive_buff_test:DUT:datafile[2]} {-radix decimal} {:receive_buff_test:DUT:datafile[1]} {-radix decimal} {:receive_buff_test:DUT:datafile[0]} {-radix decimal}} :receive_buff_test:DUT:datafile
add wave -noupdate -expand -group dut -radix decimal -childformat {{{:receive_buff_test:DUT:tagfile[7]} -radix decimal} {{:receive_buff_test:DUT:tagfile[6]} -radix decimal} {{:receive_buff_test:DUT:tagfile[5]} -radix decimal} {{:receive_buff_test:DUT:tagfile[4]} -radix decimal} {{:receive_buff_test:DUT:tagfile[3]} -radix decimal} {{:receive_buff_test:DUT:tagfile[2]} -radix decimal} {{:receive_buff_test:DUT:tagfile[1]} -radix decimal} {{:receive_buff_test:DUT:tagfile[0]} -radix decimal}} -subitemconfig {{:receive_buff_test:DUT:tagfile[7]} {-radix decimal} {:receive_buff_test:DUT:tagfile[6]} {-radix decimal} {:receive_buff_test:DUT:tagfile[5]} {-radix decimal} {:receive_buff_test:DUT:tagfile[4]} {-radix decimal} {:receive_buff_test:DUT:tagfile[3]} {-radix decimal} {:receive_buff_test:DUT:tagfile[2]} {-radix decimal} {:receive_buff_test:DUT:tagfile[1]} {-radix decimal} {:receive_buff_test:DUT:tagfile[0]} {-radix decimal}} :receive_buff_test:DUT:tagfile
add wave -noupdate -expand -group dut :receive_buff_test:DUT:validfile
add wave -noupdate -expand -group dut :receive_buff_test:DUT:empty
add wave -noupdate -expand -group dut :receive_buff_test:DUT:full
add wave -noupdate -expand -group dut :receive_buff_test:DUT:match
add wave -noupdate -divider <NULL>
add wave -noupdate -expand -group rbif :receive_buff_test:rbif:ren
add wave -noupdate -expand -group rbif :receive_buff_test:rbif:wen
add wave -noupdate -expand -group rbif :receive_buff_test:rbif:empty
add wave -noupdate -expand -group rbif :receive_buff_test:rbif:full
add wave -noupdate -expand -group rbif :receive_buff_test:rbif:hit
add wave -noupdate -expand -group rbif -radix decimal :receive_buff_test:rbif:data_in
add wave -noupdate -expand -group rbif -radix decimal :receive_buff_test:rbif:tag_in
add wave -noupdate -expand -group rbif -radix decimal :receive_buff_test:rbif:data_out
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {73 ns} 0}
quietly wave cursor active 1
configure wave -namecolwidth 262
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
WaveRestoreZoom {0 ns} {119 ns}
