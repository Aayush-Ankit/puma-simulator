// EDRAM Controller (Parameteric: #IMAs to serve/arbitrate etc.see interface file)
/*
1. Receives ren/wen from all imas and decides whom to give access
2. Upon access, the master IMA will put the contents (addr/addr) on the shared bus (conencting IMA to edram)
3. Upon completing access the controller will deassert the wait for the IMA
4. Only holds the validfile, (Data array and counter array are parts of EDRAM (from CACTI))
*/

`include "edram_controller_if.vh"

module edram_controller (input logic clk, input logic nrst,
                        edram_controller_if ecif);

    // Instatiate valid file
    logic [EDRAM_SIZE-1:0] validfile;

    // Internal Variables
    state_t state;
    logic [MEM_LAT-1:0] counter;
    logic [NUM_IMA-1:0] last_idx;

    // rearranging ren, wen, validfile for ease of verilog programming
    logic [NUM_IMA-1:0] ren_rel, wen_rel;
    logic [NUM_IMA-1:0] [ADDR_WIDTH-1:0] addr_rel;

    // generate statement - syntehsizable
    for (genvar i=0; i<NUM_IMA; i++) begin
        assign ren_rel[i] = ecif.ima_ren[(last_idx+i+1) % NUM_IMA];
        assign wen_rel[i] = ecif.ima_wen[(last_idx+i+1) % NUM_IMA];
        assign addr_rel[i] = ecif.ima_addr[(last_idx+i+1) % NUM_IMA];
    end

    // output logic
    assign ecif.ram_ren = (state == BUSY) & ecif.ima_ren[last_idx];
    assign ecif.ram_wen = (state == BUSY) & ecif.ima_wen[last_idx];
    assign ecif.ram_addr = (state == BUSY) ? ecif.ima_addr[last_idx] : 0;
    assign ecif.ram_data = ((state == BUSY) & ecif.ima_wen[last_idx]) ?
                           ecif.ima_data[last_idx] : 0;

    for (genvar i=0; i<NUM_IMA; i++) begin
        assign ecif.ima_wait[i] = ~((state == FREE) & (last_idx == i));
    end

    // State machine
    always_ff @ (posedge clk, negedge nrst) begin
        if (!nrst) begin
            validfile <= '{default:0};
            state <= FREE;
            counter <= 0;
            last_idx <= '{default:1};
        end
        else if ((state == FREE) &  ((|ecif.ima_ren) | (|ecif.ima_wen))) begin
            // select the ima to serve - needs to be parametric block
            if ((ren_rel[0] & validfile[addr_rel[0]]) | (wen_rel[0] & ~validfile[addr_rel[0]])) begin
                last_idx <= (last_idx+1) % NUM_IMA;
                state <= BUSY;
                if (ren_rel[0] & validfile[addr_rel[0]])
                    validfile[addr_rel[0]] <= 0; // worst case - when read edram_counter was 1
                    // decrements the read edram_counter
                else
                    validfile[addr_rel[0]] <= 1;
            end
            else if ((ren_rel[1] & validfile[addr_rel[1]]) | (wen_rel[1] & ~validfile[addr_rel[1]])) begin
                last_idx <= (last_idx+2) % NUM_IMA;
                state <= BUSY;
                if (ren_rel[1] & validfile[addr_rel[1]])
                    validfile[addr_rel[1]] <= 0; // worst case - when read edram_counter was 1
                    // decrements the read edram_counter
                else
                    validfile[addr_rel[1]] <= 1;
            end
            else if ((ren_rel[2] & validfile[addr_rel[2]]) | (wen_rel[2] & ~validfile[addr_rel[2]])) begin
                last_idx <= (last_idx+3) % NUM_IMA;
                state <= BUSY;
                if (ren_rel[2] & validfile[addr_rel[2]])
                    validfile[addr_rel[2]] <= 0; // worst case - when read edram_counter was 1
                    // decrements the read edram_counter
                else
                    validfile[addr_rel[2]] <= 1;
            end
            else if ((ren_rel[3] & validfile[addr_rel[3]]) | (wen_rel[3] & ~validfile[addr_rel[3]])) begin
                last_idx <= (last_idx+4) % NUM_IMA;
                state <= BUSY;
                if (ren_rel[3] & validfile[addr_rel[3]])
                    validfile[addr_rel[3]] <= 0; // worst case - when read edram_counter was 1
                    // decrements the read edram_counter
                else
                    validfile[addr_rel[3]] <= 1;
            end
        end
        else if ((state == BUSY) & (counter == MEM_LAT)) begin
            state <= FREE;
            counter <= 0;
        end
        else if (state == BUSY)
            counter <= counter + 1;
    end
endmodule
