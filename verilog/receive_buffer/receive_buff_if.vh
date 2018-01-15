// Receive Buffer (Tile) Interface

`ifndef RECEIVE_BUFF_IF_VH
`define RECEIVE_BUFF_IF_VH

// Define constants
parameter DATA_WIDTH = 8;
parameter TAG_WIDTH = 8; // width of neuron_id
parameter NUM_ENTRY = 8;

// Define interface
interface receive_buff_if ();

    logic ren, wen, empty, full, hit;
    logic [DATA_WIDTH-1:0] data_in; // data in
    logic [TAG_WIDTH-1:0] tag_in; // used for read/write
    logic [DATA_WIDTH-1:0] data_out; // data out

    modport rb (
        input ren, wen, data_in, tag_in,
        output empty, full, hit, data_out
    );

    modport tb (
        input  empty, full, hit, data_out,
        output ren, wen, data_in, tag_in
    );

endinterface

`endif //RECEIVE_BUFF_IF_VH
