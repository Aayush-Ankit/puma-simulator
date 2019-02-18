
#include <assert.h>
#include <string>
#include <vector>

#include "puma.h"
#include "conv-layer.h"
#include "fully-connected-layer.h"

void isolated_fully_connected_layer(Model model, std::string layerName, unsigned int in_size, unsigned int out_size) {

    // Input vector
    auto in = InputVector::create(model, "in", in_size);

    // Output vector
    auto out = OutputVector::create(model, "out", out_size);

    // Layer
    out = fully_connected_layer(model, layerName, in_size, out_size, in);

}

int main() {

    Model model = Model::create("vgg16");

    // Input
    unsigned int in_size_x = 224;
    unsigned int in_size_y = 224;
    unsigned int in_channels = 3;
    auto in_stream = InputImagePixelStream::create(model, "in_stream", in_size_x, in_size_y, in_channels);

    // Layer 1 (convolution) configurations
    unsigned int k_size_x1 = 3;
    unsigned int k_size_y1 = 3;
    unsigned int in_size_x1 = 224;
    unsigned int in_size_y1 = 224;
    unsigned int in_channels1 = 3;
    unsigned int out_channels1 = 64;

    // Layer 2 (convolution with max pool) configurations
    unsigned int k_size_x2 = 3;
    unsigned int k_size_y2 = 3;
    unsigned int in_size_x2 = 224;
    unsigned int in_size_y2 = 224;
    unsigned int in_channels2 = 64;
    unsigned int out_channels2 = 64;
    unsigned int max_pool_size_x2 = 2;
    unsigned int max_pool_size_y2 = 2;

    // Layer 3 (convolution) configurations
    unsigned int k_size_x3 = 3;
    unsigned int k_size_y3 = 3;
    unsigned int in_size_x3 =112;
    unsigned int in_size_y3 = 112;
    unsigned int in_channels3 = 64;
    unsigned int out_channels3 = 128;

    // Layer 4 (convolution with max pool) configurations
    unsigned int k_size_x4 = 3;
    unsigned int k_size_y4 = 3;
    unsigned int in_size_x4 =112;
    unsigned int in_size_y4 = 112;
    unsigned int in_channels4 = 128;
    unsigned int out_channels4 = 128;
    unsigned int max_pool_size_x4 = 2;
    unsigned int max_pool_size_y4 = 2;

    // Layer 5 (convolution) configurations
    unsigned int k_size_x5 = 3;
    unsigned int k_size_y5 = 3;
    unsigned int in_size_x5 =56;
    unsigned int in_size_y5 = 56;
    unsigned int in_channels5 = 128;
    unsigned int out_channels5 = 256;

    // Layer 6 (convolution) configurations
    unsigned int k_size_x6 = 3;
    unsigned int k_size_y6 = 3;
    unsigned int in_size_x6 =56;
    unsigned int in_size_y6 = 56;
    unsigned int in_channels6 = 256;
    unsigned int out_channels6 = 256;

    // Layer 7 (convolution with max pool) configurations
    unsigned int k_size_x7 = 3;
    unsigned int k_size_y7 = 3;
    unsigned int in_size_x7 =56;
    unsigned int in_size_y7 = 56;
    unsigned int in_channels7 = 256;
    unsigned int out_channels7 = 256;
    unsigned int max_pool_size_x7 = 2;
    unsigned int max_pool_size_y7 = 2;

    // Layer 8 (convolution) configurations
    unsigned int k_size_x8 = 3;
    unsigned int k_size_y8 = 3;
    unsigned int in_size_x8 =28;
    unsigned int in_size_y8 = 28;
    unsigned int in_channels8 = 256;
    unsigned int out_channels8 = 512;

    // Layer 9 (convolution) configurations
    unsigned int k_size_x9 = 3;
    unsigned int k_size_y9 = 3;
    unsigned int in_size_x9 =28;
    unsigned int in_size_y9 = 28;
    unsigned int in_channels9 = 512;
    unsigned int out_channels9 = 512;

    // Layer 10 (convolution with max pool) configurations
    unsigned int k_size_x10 = 3;
    unsigned int k_size_y10 = 3;
    unsigned int in_size_x10 =28;
    unsigned int in_size_y10 = 28;
    unsigned int in_channels10 = 512;
    unsigned int out_channels10 = 512;
    unsigned int max_pool_size_x10 = 2;
    unsigned int max_pool_size_y10 = 2;

    // Layer 11 (convolution) configurations
    unsigned int k_size_x11 = 3;
    unsigned int k_size_y11 = 3;
    unsigned int in_size_x11 =14;
    unsigned int in_size_y11 = 14;
    unsigned int in_channels11 = 512;
    unsigned int out_channels11 = 512;

    // Layer 12 (convolution) configurations
    unsigned int k_size_x12 = 3;
    unsigned int k_size_y12 = 3;
    unsigned int in_size_x12 =14;
    unsigned int in_size_y12 = 14;
    unsigned int in_channels12 = 512;
    unsigned int out_channels12 = 512;

    // Layer 13 (convolution with max pool) configurations
    unsigned int k_size_x13 = 3;
    unsigned int k_size_y13 = 3;
    unsigned int in_size_x13 =14;
    unsigned int in_size_y13 = 14;
    unsigned int in_channels13 = 512;
    unsigned int out_channels13 = 512;
    unsigned int max_pool_size_x13 = 2;
    unsigned int max_pool_size_y13 = 2;

    // Output
    unsigned int out_size_x = 7;
    unsigned int out_size_y = 7;
    unsigned int out_channels = 512;
    auto out_stream = OutputImagePixelStream::create(model, "out_stream", out_size_x, out_size_y, out_channels);

    // Layer 14 (fully-connected) configurations
    unsigned int in_size14 = 25088;
    unsigned int out_size14 = 4096;

    // Layer 15 (fully-connected) configurations
    unsigned int in_size15 = 4096;
    unsigned int out_size15 = 4096;

    // Layer 16 (fully-connected) configurations
    unsigned int in_size16 = 4096;
    unsigned int out_size16 = 1000;

    // Define network
    // FIXME: Convolution layer with padding
    auto out1 = conv_layer(model, "layer" + std::to_string(1), k_size_x1, k_size_y1, in_size_x1, in_size_y1, in_channels1, out_channels1, in_stream);
    auto out2 = convmax_layer(model, "layer" + std::to_string(2), k_size_x2, k_size_y2, in_size_x2, in_size_y2, in_channels2, out_channels2, max_pool_size_x2, max_pool_size_y2, out1);
    auto out3 = conv_layer(model, "layer" + std::to_string(3), k_size_x3, k_size_y3, in_size_x3, in_size_y3, in_channels3, out_channels3, out2);
    auto out4 = convmax_layer(model, "layer" + std::to_string(4), k_size_x4, k_size_y4, in_size_x4, in_size_y4, in_channels4, out_channels4, max_pool_size_x4, max_pool_size_y4, out3);
    auto out5 = conv_layer(model, "layer" + std::to_string(5), k_size_x5, k_size_y5, in_size_x5, in_size_y5, in_channels5, out_channels5, out4);
    auto out6 = conv_layer(model, "layer" + std::to_string(6), k_size_x6, k_size_y6, in_size_x6, in_size_y6, in_channels6, out_channels6, out5);
    auto out7 = convmax_layer(model, "layer" + std::to_string(7), k_size_x7, k_size_y7, in_size_x7, in_size_y7, in_channels7, out_channels7, max_pool_size_x7, max_pool_size_y7, out6);
    auto out8 = conv_layer(model, "layer" + std::to_string(8), k_size_x8, k_size_y8, in_size_x8, in_size_y8, in_channels8, out_channels8, out7);
    auto out9 = conv_layer(model, "layer" + std::to_string(9), k_size_x9, k_size_y9, in_size_x9, in_size_y9, in_channels9, out_channels9, out8);
    auto out10 = convmax_layer(model, "layer" + std::to_string(10), k_size_x10, k_size_y10, in_size_x10, in_size_y10, in_channels10, out_channels10, max_pool_size_x10, max_pool_size_y10, out9);
    auto out11 = conv_layer(model, "layer" + std::to_string(11), k_size_x11, k_size_y11, in_size_x11, in_size_y11, in_channels11, out_channels11, out10);
    auto out12 = conv_layer(model, "layer" + std::to_string(12), k_size_x12, k_size_y12, in_size_x12, in_size_y12, in_channels12, out_channels12, out11);
    auto out13 = convmax_layer(model, "layer" + std::to_string(13), k_size_x13, k_size_y13, in_size_x13, in_size_y13, in_channels13, out_channels13, max_pool_size_x13, max_pool_size_y13, out12);
    out_stream = out13;
    // FIXME: Transition from convolution to fully-connected (vector stream to single vector)
    isolated_fully_connected_layer(model, "layer" + std::to_string(14), in_size14, out_size14);
    isolated_fully_connected_layer(model, "layer" + std::to_string(15), in_size15, out_size15);
    isolated_fully_connected_layer(model, "layer" + std::to_string(16), in_size16, out_size16);

    // Compile
    model.compile();

    // Destroy model
    model.destroy();

    return 0;

}

