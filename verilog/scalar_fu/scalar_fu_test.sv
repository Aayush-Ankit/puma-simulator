/// Testbench for Scalar Fucntional Unit
`timescale 1ns/1ns

`include "scalar_fu_if.vh"

module scalar_fu_test;
    //DUT and Interface Instantiation
    scalar_fu_if scif ();
    scalar_fu DUT (scif);

    //Test Program
    test PROG (.tbif(scif));
endmodule

program test (scalar_fu_if tbif);
    initial begin
        parameter PERIOD = 10;
        #PERIOD tbif.a = 1; tbif. b = -2; tbif.c = 0; tbif.aluop = ADD;
        #PERIOD tbif.a = 1; tbif. b = 2; tbif.c = 1; tbif.aluop = SNA;
        #PERIOD tbif.a = -2; tbif. b = -3; tbif.c = 0; tbif.aluop = MUL;
        #PERIOD tbif.a = -4; tbif. b = 1; tbif.c = 0; tbif.aluop = LSH;
        #PERIOD tbif.a = -6; tbif. b = 1; tbif.c = 0; tbif.aluop = RSH;
        #PERIOD $finish;
   end
endprogram
