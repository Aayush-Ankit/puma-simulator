#include "puma.h"

int main(int argc, char** argv) {

    Model model = Model::create("mlpPantherBig");

    // Process parameters
    unsigned int in_size = 1024;
    unsigned int hidden_size1 = 512;
    unsigned int hidden_size2 = 1024;
    unsigned int hidden_size3 = 768;
    unsigned int out_size = 10;
    unsigned int batch_size = 1;

    // Layer matrixes
    TrainingMatrix mat1 = TrainingMatrix::create(model, "mat1", in_size, hidden_size1);
    TrainingMatrix mat2 = TrainingMatrix::create(model, "mat2", hidden_size1, hidden_size2);
    TrainingMatrix mat3 = TrainingMatrix::create(model, "mat3", hidden_size2, hidden_size3);
    TrainingMatrix mat4 = TrainingMatrix::create(model, "mat4", hidden_size3, out_size);

    for(unsigned int b = 0; b < batch_size; ++b) {

        // Input
        auto x_in = InputVector::create(model, "x_in" + std::to_string(b), in_size);
        auto y_in = InputVector::create(model, "y_in" + std::to_string(b), out_size);

        // Output
        auto out = OutputVector::create(model, "out" + std::to_string(b), out_size);

        // Forward pass - layer 1
        auto x1 = mat1 * x_in;
        auto x1_act = relu(x1);

        // Forward pass - layer 2
        auto x2 = mat2 * x1_act;
        auto x2_act = relu(x2);

        // Forward pass - layer 3
        auto x3 = mat3 * x2_act;
        auto x3_act = relu(x3);

        // Forward pass - layer 4
        auto x4 = mat4 * x3_act;
        auto x4_act = relu(x4);
        out = x4_act;

        // Error
        auto error = x4_act - y_in;
        auto loss = relu(error);

        // Backward pass - layer 4
        auto d4_temp = relu(loss); // derivative of loss - relu is just placeholder for VFU in emulator
        auto d4 = relu(d4_temp); // derivative of act - reclu is just placeholder for VFU in emulator
        auto d3_temp = Transpose(mat4)*d4;
        auto d3 = relu(d3_temp);

        // Backward pass - layer 3
        auto d2_temp = Transpose(mat3)*d3;
        auto d2 = relu(d2_temp);

        // Backward pass - layer 2
        auto d1_temp = Transpose(mat2)*d2;
        auto d1 = relu(d1_temp);

        // Weight Update
        float a = 0.01;
        mat4 -= OuterProduct(a*d4, x3);
        mat3 -= OuterProduct(a*d3, x2);
        mat2 -= OuterProduct(a*d2, x1);
        mat1 -= OuterProduct(a*d1, x_in);

    }

    // Compile
    CompilerOptions options;
    options.printDebugInfo_ = true;
    //options.coalesceMVMOperations_ = false;
    model.compile(options);

    return 0;

}
