
#include <string>
#include <vector>

#include "puma.h"
#include "lstm-layer.h"
#include "fully-connected-layer.h"

int main() {

    Model model = Model::create("bigLSTM");

    // Input
    unsigned int in_size = 8192;
    auto in = InputVector::create(model, "in", in_size);

    // Layer 1 configurations
    unsigned int in_size1 = in_size;
    unsigned int h_size1 = 8192;
    unsigned int out_size1 = 8192;

    // Layer 2 (linear layer) configurations
    unsigned int in_size2 = out_size1;
    unsigned int out_size2 = 1024;

    // Layer 3 configurations
    unsigned int in_size3 = out_size1;
    unsigned int h_size3 = 8192;
    unsigned int out_size3 = 8192;

    // Layer 4 (linear layer) configurations
    unsigned int in_size4 = out_size3;
    unsigned int out_size4 = 1024;

    // Output
    unsigned int out_sizeA = out_size2;
    unsigned int out_sizeB = out_size4;
    auto outA = OutputVector::create(model, "outA", out_sizeA);
    auto outB = OutputVector::create(model, "outB", out_sizeA);

    // Define network
    auto out1 = lstm_layer(model, "layer" + std::to_string(1), in_size1, h_size1, out_size1, in);
    auto out2 = fully_connected_layer(model, "layer" + std::to_string(2), in_size2, out_size2, out1);
    outA = out2;
    auto out3 = lstm_layer(model, "layer" + std::to_string(3), in_size3, h_size3, out_size3, out1);
    auto out4 = fully_connected_layer(model, "layer" + std::to_string(4), in_size4, out_size4, out3);
    outB = out4;

    // Compile
    model.compile();

    // Destroy model
    model.destroy();

    return 0;

}

