import numpy as np
import random
random.seed(1)
num_inputs = 30000

data = np.random.randn(num_inputs)
counter = 100* np.ones (num_inputs)
valid = np.ones (num_inputs)
inp = {'data':data, 'counter': counter, 'valid':valid}
filename = 'input.npy'
np.save (filename, inp)
