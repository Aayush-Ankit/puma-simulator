/*
 *  Copyright (c) 2019 IMPACT Research Group, University of Illinois.
 *  All rights reserved.
 *
 *  This file is covered by the LICENSE.txt license file in the root directory.
 *
 */

#ifndef _PUMA_TEST_CONV_LAYER_
#define _PUMA_TEST_CONV_LAYER_

#include "puma.h"

static ImagePixelStream conv_layer(Model model, std::string layerName, unsigned int k_size_x, unsigned int k_size_y, unsigned int in_size_x, unsigned int in_size_y, unsigned int in_channels, unsigned int out_channels, unsigned int stride, unsigned int out_size_x, unsigned int out_size_y, ImagePixelStream in_stream) {

    ConvolutionalConstantMatrix mat = ConvolutionalConstantMatrix::create(model, layerName + "conv_mat", k_size_x, k_size_y, in_channels, out_channels, stride, out_size_x, out_size_y);

    return sig(mat*in_stream);

}

static ImagePixelStream convmax_layer(Model model, std::string layerName, unsigned int k_size_x, unsigned int k_size_y, unsigned int in_size_x, unsigned int in_size_y, unsigned int in_channels, unsigned int out_channels, unsigned int stride, unsigned int out_size_x, unsigned int max_pool_size_x, unsigned int max_pool_size_y, ImagePixelStream in_stream) {

    ConvolutionalConstantMatrix mat = ConvolutionalConstantMatrix::create(model, layerName + "conv_mat", k_size_x, k_size_y, in_channels, out_channels, stride, out_size_x, out_size_x);

    return maxpool(sig(mat*in_stream), max_pool_size_y, max_pool_size_x);

}

#endif

