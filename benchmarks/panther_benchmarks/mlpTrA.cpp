#include "puma.h"

int main(int argc, char** argv) {

    Model model = Model::create("mlpTrA");

    // Process parameters
    unsigned int in_size = 512;
    unsigned int hidden_size = 512;
    unsigned int out_size = 512;
    unsigned int batch_size = 1;

    // Layer matrixes
    TrainingMatrix mat1 = TrainingMatrix::create(model, "mat1", in_size, hidden_size);
    TrainingMatrix mat2 = TrainingMatrix::create(model, "mat2", hidden_size, out_size);

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
        out = x2_act;

        // Error
        auto error = x2_act - y_in;
        auto loss = relu(error);

        // Backward pass - layer 2
        auto d2_temp = relu(loss);
        auto d2 = relu(d2_temp);
        auto d1_temp = Transpose(mat2)*d2;
        auto d1 = relu(d1_temp);

        // Weight Update
        float a = 0.01;
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
