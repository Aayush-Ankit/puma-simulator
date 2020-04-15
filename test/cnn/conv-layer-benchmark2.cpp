/*
 *  Copyright (c) 2019 IMPACT Research Group, University of Illinois.
 *  All rights reserved.
 *
 *  This file is covered by the LICENSE.txt license file in the root directory.
 *
 */

#include <assert.h>
#include <string>
#include <vector>

#include "puma.h"
#include "conv-layer.h"

int main(int argc, char** argv) {

    Model model = Model::create("conv2-layer");

    // Process parameters
    unsigned int in_size_x = 5;
    unsigned int in_size_y = 5;
    unsigned int in_channels = 256;
    unsigned int out_channels = 256;
    unsigned int k_size_x = 3;
    unsigned int k_size_y = 3;
    if(argc == 7) {
        in_size_x = atoi(argv[1]);
        in_size_y = atoi(argv[2]);
        in_channels = atoi(argv[3]);
        out_channels = atoi(argv[4]);
        k_size_x = atoi(argv[5]);
        k_size_y = atoi(argv[6]);
    }

    // Input stream
    auto in_stream = InputImagePixelStream::create(model, "in_stream", in_size_x, in_size_y, in_channels);

    // Output stream
    unsigned int out_size_x = in_size_x;
    unsigned int out_size_y = in_size_y;
    auto out_stream = OutputImagePixelStream::create(model, "out_stream", out_size_x, out_size_y, out_channels);

    // Layer
    out_stream = conv_layer(model, "", k_size_x, k_size_y, in_size_x, in_size_y, in_channels, out_channels, in_stream);

    // Compile
    model.compile();

    // Destroy model
    model.destroy();

    return 0;

}

