// Simulate a matrix size of Layer9 (same repeats from 9-13) of Vgg16 -

#include "puma.h"

int main(int argc, char** argv) {

    Model model = Model::create("convBPanther");

    // Process parameters
    unsigned int in_size = 2304;
    unsigned int out_size = 256;
    unsigned int batch_size = 1;

    // Layer matrixes
    TrainingMatrix mat1 = TrainingMatrix::create(model, "mat1", in_size, out_size);

    for(unsigned int b = 0; b < batch_size; ++b) {

        // Input
        auto x_in = InputVector::create(model, "x_in" + std::to_string(b), in_size);
        auto y_in = InputVector::create(model, "y_in" + std::to_string(b), out_size);

        // Output
        auto out = OutputVector::create(model, "out" + std::to_string(b), out_size);
        auto out1 = OutputVector::create(model, "out1" + std::to_string(b), in_size);

        // Forward pass - layer 1
        auto x1 = mat1 * x_in;
        auto x1_act = relu(x1);
        out = x1_act;

        // Error
        auto error = x1_act - y_in;
        auto loss = relu(error);

        // Backward pass - layer 1
        auto d2_temp = relu(loss); // derivative of loss - relu is just placeholder for VFU in emulator
        auto d2 = relu(d2_temp); // derivative of act - reclu is just placeholder for VFU in emulator

        auto d1_temp = Transpose(mat1)*d2;
        auto d1 = relu(d1_temp);
        out1 = d1;

        // Weight Update
        float a = 0.01;
        mat1 -= OuterProduct(a*d2, x_in);

    }

    // Compile
    CompilerOptions options;
    options.printDebugInfo_ = true;
    //options.coalesceMVMOperations_ = false;
    model.compile(options);

    return 0;

}
