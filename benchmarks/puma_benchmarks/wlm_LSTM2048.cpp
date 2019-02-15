
#include <string>
#include <vector>

#include "puma.h"
#include "lstm-layer.h"
#include "fully-connected-layer.h"

int main() {

    Model model = Model::create("LSTM2048");

    // Input
    unsigned int in_size = 8192;
    auto in = InputVector::create(model, "in", in_size);

    // Layer 1 configurations
    unsigned int in_size1 = in_size;
    unsigned int h_size1 = 8192;
    unsigned int out_size1 = 8192;

    // Layer 2 (linear layer) configurations
    unsigned int in_size2 = out_size1;
    unsigned int out_size2 = 2048;

    // Output
    unsigned int out_size = out_size2;
    auto out = OutputVector::create(model, "out", out_size);

    // Define network
    auto out1 = lstm_layer(model, "layer" + std::to_string(1), in_size1, h_size1, out_size1, in);
    auto out2 = fully_connected_layer(model, "layer" + std::to_string(2), in_size2, out_size2, out1);
    out = out2;

    // Compile
    model.compile();

    // Destroy model
    model.destroy();

    return 0;

}

