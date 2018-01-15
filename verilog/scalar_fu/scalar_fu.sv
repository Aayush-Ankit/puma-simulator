// Scalar Function Unit (Parameteric: #bits (4,8,12,16)) for DPE

`include "scalar_fu_if.vh"

module scalar_fu (scalar_fu_if scif);

    always_comb begin
        case (scif.aluop)
            ADD: scif.out = scif.a + scif.b;
            SNA: scif.out = scif.a + (scif.b << scif.c);
            MUL: scif.out = scif.a * scif.b;
            LSH: scif.out = scif.a <<< scif.b;
            RSH: scif.out = scif.a >>> scif.b;
            default: scif.out = 0;
        endcase
    end

endmodule
