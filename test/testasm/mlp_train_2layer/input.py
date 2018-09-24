import numpy as np
import random
random.seed(1)
num_inputs = 512

data = np.random.rand(num_inputs)
counter = 10* np.ones (num_inputs)
valid = np.ones (num_inputs)
inp = {'data':data, 'counter': counter, 'valid':valid}
filename = 'input.npy'
np.save (filename, inp)
