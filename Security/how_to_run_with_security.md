# Security and multi-model implementation
This document describes alterations made to the compiler and simulator of the PUMA machine learning accelerator that allows it to execute multiple models concurrently and with more security.


- [Alterations Made](#Alterations-Made)
- [How to Add your Own Security Module](#How-to-Add-your-Own-Security-Module)
- [How to run](#how-to-run)

## Alterations Made

Two different solutions for security were implemented, first a MAC(Message Authentication Code) was implemented to validate models received by the architecture and secondly a model encryption approach was developed to allow the model to be securely sent to the simulator.

For the security module, we implemented two interfaces that allow for different implementations of cryptography and authentication methods. We also made one implementation for each interface, the first one was for authentication and uses a SHA256 hash to generate a hash of the model and the input and then we used the Fernet python library to encrypt the hash generating a MAC. The Fernet library was also used for the encryption/decryption of models. We also created a factory class in order to make adding new security models easier. Other alterations made to run models securely were in the source file dpe.py in which two parameters -a and -c that allow the simulator to run authenticated models “-a” or encrypted models “-c” were added.

  
![image](https://user-images.githubusercontent.com/2287889/75450667-fe2df500-594d-11ea-9f75-e55f2af90448.png)

Figure 1: UML Diagram showing the relations between the Security classes.

To make possible the use of a multi-model in PUMA, we implemented the pre-compiler approach, with the creation of one C++ file, carrying the task of fusing selected ML models and compile them together. The result of this process is a single model that is suitable to run in the simulator. The multi-model approach implies better resource utilization, energy efficiency, and performance to the accelerator when compared to sequential execution. The whole process became possible with the creation of a C++ header file, which has all models available in the compiler, thus making possible the utilization of multi-models in one file.

## How to Add your Own Security Module

To add your own security module first you will need to make sure that it implements all functions provided by either the ICryptography interface or the IAuth interface. After you will need to add a call to your class in the Factory class so that when the factory is called with the name of your security solution as an argument it will use the methods implemented by it.

## How to Run

This section contains the instructions to properly execute the compiler and simulator with the implemented security modules and multi-model. To set up the simulation environment first one has to download the PUMA Compiler, Simulator and Python in Ubuntu 16 or above.

After this first step open a terminal and navigate to the simulator folder and run the following commands to install all python libraries needed

  
  

`$ sudo apt-get install python-tk`

`$ sudo pip install http://download.pytorch.org/whl/cu80/torch-0.3.0.post4-cp27-cp27mu-linux_x86_64.whl`

`$ sudo pip install -r requirements.txt`

You now have to edit the test/utils/generate-py.sh and the test/utils/populate.py file changing the simulator_path variable to point to your simulator root path. Then in the test/utils folder, copy the files generate-py.sh and input.py to puma-compiler/test. With the simulator’s dependencies done, now you have to set the environment in the compilator, to these steps, navigate to the compiler folder. First, you have to compile the files in the src folder, to do so:

  

`$ cd src/`

`$ make`

  

Now you have to set the path of this src folder as the library path of the compiler, then follow the steps.

  

``$ export LD_LIBRARY_PATH=`pwd`:$LD_LIBRARY_PATH``

  

To compile a Model you will have to go to the test folder

`$ cd ../test`

`$ make <desired  model>.cpp`

`$ ./<desired  model>.test`

  

To run multi-model with the pre-compiler approach, follow the steps:

  

`$ make pre_compiler.cpp`

`$ ./pre_compiler.test <model1>  <model2> …`

  

The models passed as arguments will be fused, generating one model containing the instructions of the selected models.

  

Finally, to organize the generated files (separate tiles instructions and generate model’s input), run the following script:

  

`$ ./generate-py.sh (-c <cypher> for cryptography or -a <cypher_hash> authentication optional)`

  

Here, are some examples of how to execute the security modules implemented:

  

`$ ./generate-py.sh -c Fernet`

  

`$ ./generate-py.sh -a Fer256`

After doing these steps there will be a folder with the name of the desired model in the /test folder you should copy this folder to the simulator /test/testasm folder with the following command:

  

`$ cp -R <desired  model  folder> puma-simulator/test/testasm/`

Now you’re ready to run the simulation, go to the simulator /src folder and run the dpe.py script

`$ python dpe.py -n <model  name> (-c <cypher> or -a <cypher_hash> for cryptography or authentication)`

Once the simulation ends, the results and all states achieved during the process will be stored at the directory test/traces/model_name. The file hardware_stats.txt contains general information around the hardware, cycles of computation, and energy consumption. The information about EDRAM contents can be found at the file output.txt, and for each tile will be generated a folder that has the trace of all cycles utilized during the simulation.
