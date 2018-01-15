// Scalar Function Unit (IMA) Interface

`ifndef SCALAR_FU_IF_VH
`define SCALAR_FU_IF_VH

// Define constants
parameter DATA_WIDTH = 8;
parameter ALUOP_WIDTH = 3;

typedef enum logic [ALUOP_WIDTH-1:0] {
    ADD,
    SNA,
    MUL,
    LSH,
    RSH
} aluop_t;

// Define interface
interface scalar_fu_if ();

    logic signed [DATA_WIDTH-1:0] a, b, c; // data in
    aluop_t aluop;
    logic signed [2*(DATA_WIDTH)-1:0] out; // data out

    modport sc (
        input a, b, aluop,
        output out
    );

    modport tb (
        input out,
        output a, b, aluop
    );

endinterface

`endif //SCALAR_FU_IF_VH
