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
#include <iostream>

#include "puma.h"
#include "conv-layer.h"
using namespace std;
int main(int argc, char** argv) {

//    Model model = Model::create("conv3-layer");

    // Process parameter
    unsigned int in_size_x ; 
    unsigned int in_size_y ; 
    unsigned int in_channels ;
    unsigned int out_channels ;
    unsigned int k_size_x ;
    unsigned int k_size_y ;
    unsigned int padding ;
    unsigned int stride ;

    if(argc == 10) {
        in_size_x = atoi(argv[1]);
        in_size_y = atoi(argv[2]);
        in_channels = atoi(argv[3]);
        out_channels = atoi(argv[4]);
        k_size_x = atoi(argv[5]);
        k_size_y = atoi(argv[6]);
		padding = atoi(argv[7]);
		stride = atoi(argv[8]);
    }    
    std:: string str=std::string("conv") + argv[9] + std::string("-layer");
    Model model = Model::create(str);
   
    // Input stream
    auto in_stream = InputImagePixelStream::create(model, "in_stream", in_size_x, in_size_y, in_channels);

    // Output stream
    unsigned int out_size_x = (in_size_x - k_size_x + 2*padding)/stride + 1;
    unsigned int out_size_y =  (in_size_y - k_size_y + 2*padding)/stride + 1;
   
   	assert((in_size_x - k_size_x + 2*padding)%stride==0); //input image size should result in integer out image size
    auto out_stream = OutputImagePixelStream::create(model, "out_stream", out_size_x, out_size_y, out_channels);
    
    // Layer
    out_stream = conv_layer(model, "", k_size_x, k_size_y, in_size_x, in_size_y, in_channels, out_channels, stride, out_size_x, out_size_y, in_stream);
    // Compile
    model.compile();

    // Destroy model
    model.destroy();

    return 0;

}

