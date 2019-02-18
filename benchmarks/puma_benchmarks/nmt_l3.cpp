
#include <string>
#include <vector>

#include "puma.h"
#include "lstm-layer.h"
#include "fully-connected-layer.h"

int main() {

    Model model = Model::create("nmt-l3");

    // Input
    unsigned int in_size = 1024;
    auto in = InputVector::create(model, "in", in_size);

    // Layer 1 configurations
    unsigned int in_size1 = in_size;
    unsigned int h_size1 = 1024;
    unsigned int out_size1 = 1024;

    // Layer 2 configurations
    unsigned int in_size2 = out_size1;
    unsigned int h_size2 = 1024;
    unsigned int out_size2 = 1024;

    // Layer 3 configurations
    unsigned int in_size3 = out_size2;
    unsigned int h_size3 = 1024;
    unsigned int out_size3 = 1024;

    // Layer 4 configurations
    unsigned int in_size4 = out_size3;
    unsigned int h_size4 = 1024;
    unsigned int out_size4 = 1024;

    // Layer 5 configurations
    unsigned int in_size5 = out_size4;
    unsigned int h_size5 = 1024;
    unsigned int out_size5 = 1024;

    // Layer 6 configurations
    unsigned int in_size6 = out_size5;
    unsigned int h_size6 = 1024;
    unsigned int out_size6 = 1024;

    // Layer 7 (linear layer) configurations
    unsigned int in_size7 = out_size6;
    unsigned int out_size7 = 40000;

    // Output
    unsigned int out_size = out_size7;
    auto out = OutputVector::create(model, "out", out_size);

    // Define network
    auto out1 = lstm_layer(model, "layer" + std::to_string(1), in_size1, h_size1, out_size1, in);
    auto out2 = lstm_layer(model, "layer" + std::to_string(2), in_size2, h_size2, out_size2, out1);
    auto out3 = lstm_layer(model, "layer" + std::to_string(3), in_size3, h_size3, out_size3, out2);
    auto out4 = lstm_layer(model, "layer" + std::to_string(4), in_size4, h_size4, out_size4, out3);
    auto out5 = lstm_layer(model, "layer" + std::to_string(5), in_size5, h_size5, out_size5, out4);
    auto out6 = lstm_layer(model, "layer" + std::to_string(6), in_size6, h_size6, out_size6, out5);
    auto out7 = fully_connected_layer(model, "layer" + std::to_string(7), in_size7, out_size7, out6);
    out = out7;

    // Compile
    model.compile();

    // Destroy model
    model.destroy();

    return 0;

}

