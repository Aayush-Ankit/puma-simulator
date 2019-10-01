/*
 *  Copyright (c) 2019 IMPACT Research Group, University of Illinois.
 *  All rights reserved.
 *
 *  This file is covered by the LICENSE.txt license file in the root directory.
 *
 */

#include<iostream>
#include<fstream>
//#include<string>
#include "puma.h"
#include "fully-connected-layer.h"

int main() {

    Model model = Model::create("mlp-l4-mnist");

    // Input
    unsigned int in_size = 784;
    auto in = InputVector::create(model, "in", in_size);

    // Layer 1 configurations
    unsigned int in_size1 = in_size;
    unsigned int out_size1 = 1024;

    // Layer 2 configurations
    unsigned int in_size2 = out_size1;
    unsigned int out_size2 = 512;

    // Layer 3 configurations
    unsigned int in_size3 = out_size2;
    unsigned int out_size3 = 200;

    // Layer 4 configurations
    unsigned int in_size4 = out_size3;
    unsigned int out_size4 = 10;

    // Output
    unsigned int out_size = out_size4;
    auto out = OutputVector::create(model, "out", out_size);

    // Define network
    auto out1 = fully_connected_layer(model, "layer" + std::to_string(1), in_size1, out_size1, in);
    auto out2 = fully_connected_layer(model, "layer" + std::to_string(2), in_size2, out_size2, out1);
    auto out3 = fully_connected_layer(model, "layer" + std::to_string(3), in_size3, out_size3, out2);
    auto out4 = fully_connected_layer(model, "layer" + std::to_string(4), in_size4, out_size4, out3);
    out = out4;

    // Compile
    model.compile();

    // Bind data
    ModelInstance modelInstance = ModelInstance::create(model);
    float* layer1Weights = new float[in_size1*out_size1];
    float* layer2Weights = new float[in_size2*out_size2];
    float* layer3Weights = new float[in_size3*out_size3];
    float* layer4Weights = new float[in_size4*out_size4];

    // Hardcoding weights
    /*for(int i=0; i< in_size1*out_size1 ; i++){
	    layer1Weights[i] = 1.5 ;
       }

    for(int i=0; i< in_size2*out_size2 ; i++){
	    layer2Weights[i] = 1.5 ;
       }

    for(int i=0; i< in_size3*out_size3 ; i++){
	    layer3Weights[i] = 1.5 ;
       }

    for(int i=0; i< in_size4*out_size4 ; i++){
	    layer4Weights[i] = 1.5 ;
       }*/

    //Reading weights from text files
    int i=0;
    std::ifstream wf1;
    wf1.open("mlp_l4_mnist_weights/wl1.txt");
    while(wf1 >> layer1Weights[i])
    { i++; }
    wf1.close();

    i=0;
    std::ifstream wf2;
    wf2.open("mlp_l4_mnist_weights/wl2.txt");
    while(wf2 >> layer2Weights[i])
    { i++; }
    wf2.close();

    i=0;
    std::ifstream wf3;
    wf3.open("mlp_l4_mnist_weights/wl3.txt");
    while(wf3 >> layer3Weights[i])
    { i++; }
    wf3.close();

    i=0;
    std::ifstream wf4;
    wf4.open("mlp_l4_mnist_weights/wl4.txt");
    while(wf4 >> layer4Weights[i])
    { i++; }
    wf4.close();
    
    /*std::cout<< "Layer 4 Weights:\n";
    for(i=0;i<in_size4*out_size4;i++)
    {
        std::cout << layer4Weights[i] << " ";
    }*/


    fully_connected_layer_bind(modelInstance, "layer" + std::to_string(1), layer1Weights);
    fully_connected_layer_bind(modelInstance, "layer" + std::to_string(2), layer2Weights);
    fully_connected_layer_bind(modelInstance, "layer" + std::to_string(3), layer3Weights);
    fully_connected_layer_bind(modelInstance, "layer" + std::to_string(4), layer4Weights);
    
    modelInstance.generateData();

    // Destroy model
    model.destroy();
    delete[] layer1Weights;
    delete[] layer2Weights;
    delete[] layer3Weights;
    delete[] layer4Weights;

    return 0;

}

