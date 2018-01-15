// Receive Buffer (Parameteric: #entries, #bits per entry)
// Synchronuous reads/writes

`include "receive_buff_if.vh"

module receive_buff (input logic clk, input logic nrst,
                  receive_buff_if rbif);

    // Insatntiate memory files - data, tag, valid
    logic [NUM_ENTRY-1:0] [DATA_WIDTH-1:0] datafile;
    logic [NUM_ENTRY-1:0] [TAG_WIDTH-1:0] tagfile;
    logic [NUM_ENTRY-1:0] validfile;

    // Internal variables
    logic empty, full;
    logic [NUM_ENTRY-1:0] match;
    assign empty = ~(|validfile);
    assign full = &validfile;

    // output logic
    assign rbif.empty = empty;
    assign rbif.full = full;
    assign rbif.hit = |match;

    // This needs to be a parameteric mux
    assign rbif.data_out = match[0] ? datafile[0] :
                           match[1] ? datafile[1] :
                           match[2] ? datafile[2] :
                           match[3] ? datafile[3] :
                           match[4] ? datafile[4] :
                           match[5] ? datafile[5] :
                           match[6] ? datafile[6] :
                           match[7] ? datafile[7] : 'x;

    always_ff @ (posedge clk, negedge nrst) begin
        if (!nrst) begin
            validfile <= '{default:0};
        end
        else begin
            // Reading the buffer
            if (rbif.ren) begin
                // check if buffer is non-empty
                if (empty)
                        match <= '{default:0};
                else begin
                    // check for tag_match - reach where the tag matches
                    match[0] <= validfile[0] & (tagfile[0] == rbif.tag_in);
                    match[1] <= validfile[1] & (tagfile[1] == rbif.tag_in);
                    match[2] <= validfile[2] & (tagfile[2] == rbif.tag_in);
                    match[3] <= validfile[3] & (tagfile[3] == rbif.tag_in);
                    match[4] <= validfile[4] & (tagfile[4] == rbif.tag_in);
                    match[5] <= validfile[5] & (tagfile[5] == rbif.tag_in);
                    match[6] <= validfile[6] & (tagfile[6] == rbif.tag_in);
                    match[7] <= validfile[7] & (tagfile[7] == rbif.tag_in);

                    // invalidate theat entry if tag hit
                    validfile[0] <= (validfile[0] & (tagfile[0] == rbif.tag_in))
                                    ? 0 : validfile[0];
                    validfile[1] <= (validfile[1] & (tagfile[1] == rbif.tag_in))
                                    ? 0 : validfile[1];
                    validfile[2] <= (validfile[2] & (tagfile[2] == rbif.tag_in))
                                    ? 0 : validfile[2];
                    validfile[3] <= (validfile[3] & (tagfile[3] == rbif.tag_in))
                                    ? 0 : validfile[3];
                    validfile[4] <= (validfile[4] & (tagfile[4] == rbif.tag_in))
                                    ? 0 : validfile[4];
                    validfile[5] <= (validfile[5] & (tagfile[5] == rbif.tag_in))
                                    ? 0 : validfile[5];
                    validfile[6] <= (validfile[6] & (tagfile[6] == rbif.tag_in))
                                    ? 0 : validfile[6];
                    validfile[7] <= (validfile[7] & (tagfile[7] == rbif.tag_in))
                                    ? 0 : validfile[7];
                end
            end
            else if (rbif.wen) begin
                if (!full) begin
                    // priority search - write at the first empty entry
                    if (!validfile[0]) begin
                        validfile[0] <= 1;
                        datafile[0] <= rbif.data_in;
                        tagfile[0] <= rbif.tag_in;
                    end
                    else if (!validfile[1]) begin
                        validfile[1] <= 1;
                        datafile[1] <= rbif.data_in;
                        tagfile[1] <= rbif.tag_in;
                    end
                    else if (!validfile[2]) begin
                        validfile[2] <= 1;
                        datafile[2] <= rbif.data_in;
                        tagfile[2] <= rbif.tag_in;
                    end
                    else if (!validfile[3]) begin
                        validfile[3] <= 1;
                        datafile[3] <= rbif.data_in;
                        tagfile[3] <= rbif.tag_in;
                    end
                    else if (!validfile[4]) begin
                        validfile[4] <= 1;
                        datafile[4] <= rbif.data_in;
                        tagfile[4] <= rbif.tag_in;
                    end
                    else if (!validfile[5]) begin
                        validfile[5] <= 1;
                        datafile[5] <= rbif.data_in;
                        tagfile[5] <= rbif.tag_in;
                    end
                    else if (!validfile[6]) begin
                        validfile[6] <= 1;
                        datafile[6] <= rbif.data_in;
                        tagfile[6] <= rbif.tag_in;
                    end
                    else  if (!validfile[7]) begin
                        validfile[7] <= 1;
                        datafile[7] <= rbif.data_in;
                        tagfile[7] <= rbif.tag_in;
                    end
                end
            end
        end
    end

endmodule
