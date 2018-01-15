/// Testbench for Scalar Fucntional Unit
`timescale 1ns/1ns

`include "edram_controller_if.vh"

module edram_controller_test;
    parameter PERIOD = 10;

    //Generate the clock
    logic CLK = 0;
    always #(PERIOD/2) CLK++;

    logic nrst;

    //DUT and Interface Instantiation
    edram_controller_if ecif ();
    edram_controller DUT (CLK, nrst, ecif);

    //Test Program
    test PROG (.CLK,
               .nrst,
               .tbif(ecif));
endmodule

program test (input logic CLK, output logic nrst, edram_controller_if tbif);
    parameter PERIOD = 10;
    initial begin
        #PERIOD nrst = 0;
        #PERIOD nrst = 1;

        // Test arbitration between writes
        #PERIOD     tbif.ima_ren = 4'b0000; tbif.ima_wen = 4'b0001; tbif.ima_addr[0] = 1; tbif.ima_data[0] = 1;
        #(5*PERIOD) tbif.ima_ren = 4'b0000; tbif.ima_wen = 4'b0010; tbif.ima_addr[1] = 2; tbif.ima_data[1] = 2;
        #(5*PERIOD) tbif.ima_ren = 4'b0000; tbif.ima_wen = 4'b0100; tbif.ima_addr[2] = 3; tbif.ima_data[2] = 3;
        #(5*PERIOD) tbif.ima_ren = 4'b0000; tbif.ima_wen = 4'b1000; tbif.ima_addr[3] = 4; tbif.ima_data[3] = 4;

        // Test arbitration between reads
        #(5*PERIOD) tbif.ima_ren = 4'b1001; tbif.ima_wen = 4'b0000; tbif.ima_addr[0] = 1; tbif.ima_data[0] = 'x; //shud read 1
        #(5*PERIOD) tbif.ima_ren = 4'b1011; tbif.ima_wen = 4'b0000; tbif.ima_addr[1] = 2; tbif.ima_data[1] = 'x; //

        // Test an request sent during BUSY state
        #(2*PERIOD) tbif.ima_ren = 4'b1111; tbif.ima_wen = 4'b0000; tbif.ima_addr[1] = 3; tbif.ima_data[1] = 'x; // nothing shud happen
        #(3*PERIOD) tbif.ima_ren = 4'b1101; tbif.ima_wen = 4'b0000; tbif.ima_addr[2] = 3; tbif.ima_data[1] = 'x; // shud read 3
        #(5*PERIOD) tbif.ima_ren = 4'b0001; tbif.ima_wen = 4'b0000; tbif.ima_addr[0] = 1; tbif.ima_data[1] = 'x; // shud read nothing - not-hit
        #(5*PERIOD) $finish;
   end
endprogram
