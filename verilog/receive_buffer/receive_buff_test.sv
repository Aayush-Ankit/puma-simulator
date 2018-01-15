/// Testbench for Scalar Fucntional Unit
`timescale 1ns/1ns

`include "receive_buff_if.vh"

module receive_buff_test;
    parameter PERIOD = 10;

    //Generate the clock
    logic CLK = 0;
    always #(PERIOD/2) CLK++;

    logic nrst;

    //DUT and Interface Instantiation
    receive_buff_if rbif ();
    receive_buff DUT (CLK, nrst, rbif);

    //Test Program
    test PROG (.CLK,
               .nrst,
               .tbif(rbif));
endmodule

program test (input logic CLK, output logic nrst, receive_buff_if tbif);
    parameter PERIOD = 10;
    initial begin
        #PERIOD nrst = 0;
        #PERIOD nrst = 1;
        // reading an empty buffer
        #PERIOD tbif.ren = 1; tbif.wen = 0; tbif.tag_in = 4; tbif.data_in = 0;
        // write and make the buffer full
        #PERIOD tbif.ren = 0; tbif.wen = 1; tbif.tag_in = 1; tbif.data_in = 1;
        #PERIOD tbif.ren = 0; tbif.wen = 1; tbif.tag_in = 2; tbif.data_in = 2;
        #PERIOD tbif.ren = 0; tbif.wen = 1; tbif.tag_in = 3; tbif.data_in = 3;
        #PERIOD tbif.ren = 0; tbif.wen = 1; tbif.tag_in = 4; tbif.data_in = 4;
        #PERIOD tbif.ren = 0; tbif.wen = 1; tbif.tag_in = 5; tbif.data_in = 5;
        #PERIOD tbif.ren = 0; tbif.wen = 1; tbif.tag_in = 6; tbif.data_in = 6;
        #PERIOD tbif.ren = 0; tbif.wen = 1; tbif.tag_in = 7; tbif.data_in = 7;
        #PERIOD tbif.ren = 0; tbif.wen = 1; tbif.tag_in = 8; tbif.data_in = 8;
        // write to a full buffer
        #PERIOD tbif.ren = 0; tbif.wen = 1; tbif.tag_in = 9; tbif.data_in = 9;
        // read from the buffer - for miss
        #PERIOD tbif.ren = 1; tbif.wen = 0; tbif.tag_in = 9; tbif.data_in = 'x;
        // read from the buffer - for hit
        #PERIOD tbif.ren = 1; tbif.wen = 0; tbif.tag_in = 4; tbif.data_in = 'x;
        // read from the buffer - miss (previously hit)
        #PERIOD tbif.ren = 1; tbif.wen = 0; tbif.tag_in = 4; tbif.data_in = 'x;
        // check an unordered write
        #PERIOD tbif.ren = 0; tbif.wen = 1; tbif.tag_in = 16; tbif.data_in = 16;
        #PERIOD $finish;
   end
endprogram
