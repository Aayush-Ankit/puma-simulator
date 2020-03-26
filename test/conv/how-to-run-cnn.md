1. Copy the sample cnnbig.cpp and paste it in puma-compiler/test/

2. Chnage the cnnbig.cpp as needed.

   NOTE: Do not change in_size_x and in_size_y
	 Only chnage the input and output channels

   If you want to simulate a conv layer for bigger input activation map, just multiply the results for this by X

  where X = (actual input height * actual input width) / ( 2 * 2)

	 	 
   In line 18, change the name as required. This is the name of 'net'

3. In puma-compiler/test/

	execute:

		make clean
		make 'net'.test
		./'net'.test
		rm -rf 'net'
		./generate-py.sh

4. Copy the 'net' directory to puma-simulator/test/testasm/

5. Copy the input.npy in puma-simulator/test/utils/ and paste it in puma-simulator/test/testasm/'net'/


		 
