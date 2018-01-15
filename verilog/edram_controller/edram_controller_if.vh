// EDRAM Controller (Tile) Interface

`ifndef EDRAM_CONTROLLER_IF_VH
`define EDRAM_CONTROLLER_IF_VH

// Define constants
parameter NUM_IMA = 4;
parameter ADDR_WIDTH = 20;
parameter DATA_WIDTH = 12; // includes data and counter
parameter EDRAM_SIZE = 32;
parameter MEM_LAT = 4;
parameter NUM_STATE = 2; // Currently: FREE, BUSY

typedef enum logic [NUM_STATE-1:0] {
    FREE,
    BUSY
} state_t;

// Define interface
interface edram_controller_if ();
    // to ima(s) side
    logic [NUM_IMA-1:0] ima_ren, ima_wen, ima_wait;
    logic [NUM_IMA-1:0] [ADDR_WIDTH-1:0] ima_addr;
    logic [NUM_IMA-1:0] [DATA_WIDTH-1:0] ima_data;

    // to edram side
    logic ram_ren, ram_wen;
    logic [ADDR_WIDTH-1:0] ram_addr;
    logic [DATA_WIDTH-1:0] ram_data;

    modport rb (
        input ima_ren, ima_wen, ima_data, ima_addr,
        output ima_wait, ram_ren, ram_wen, ram_addr,
               ram_data
    );

    modport tb (
        output ima_ren, ima_wen, ima_data, ima_addr,
        input ima_wait, ram_ren, ram_wen, ram_addr,
               ram_data
    );
endinterface

`endif //EDRAM_CONTROLLER_IF_VH
