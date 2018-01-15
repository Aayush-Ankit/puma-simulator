-- API to implement an LSTM cell
torch.setdefaulttensortype('torch.FloatTensor')
require 'nn'
require 'paths'

-- path where all traces (inputs, internal states and weights are dumped from
-- torch for testing with harwdare purposes)
tracepath = '/home/ankitaay/dpe/test/testasm/LSTM2_new/'

-- fix seed (for experiment reproducibility)
torch.manualSeed(1)

-- input and hidden state sizes
in_size = 4
h_size = 3

-- Specify the non-linearities
nl1 = nn.Sigmoid ()
nl2 = nn.Sigmoid ()

-- For LSTM cell 1 (maps to tile 1)
-- specify the transformation matices (for preactivations)
i2h_mat = torch.rand (in_size, 4 * h_size)
h2h_mat = torch.rand (h_size, 4 * h_size)
-- bias_vec = torch.rand(1, 4 * h_size)

-- specify the input and hidden state, IMA Vector LD (2 Loads)
inp_1 = torch.rand (1, in_size)
h_0 = torch.rand (1, h_size)
c_0 = torch.rand (1, h_size)

-- IMA MVM
preact_inp = inp_1 * i2h_mat
preact_h = h_0 * h2h_mat

-- IMA Vector Add
out = preact_inp + preact_h
--print (out)

-- IMA Vector Add
-- out = out + bias_vec

-- IMA Vector Non-Linear operations
i_gate = nl1:forward(out)[{{1}, {0*h_size+1, 0*h_size+h_size}}]
f_gate = nl1:forward(out)[{{1}, {1*h_size+1, 1*h_size+h_size}}]
o_gate = nl1:forward(out)[{{1}, {2*h_size+1, 2*h_size+h_size}}]
c_int = nl2:forward(out)[{{1}, {3*h_size+1, 3*h_size+h_size}}]

-- Update the cell state
-- 2 IMA  Vector multiply & 1 IMA Vector ADD
c_1 = torch.cmul (f_gate, c_0) + torch.cmul (i_gate, c_int)

-- IMA Vector Non-linearity and Vector Multiply
h_1 = torch.cmul (o_gate, nl2:forward(c_1))

print ('Time t: ' .. 'Cell state', c_1, 'Hidden state', h_1)

-- For LSTM cell 2 (maps to tile 2)
-- specify the input and hidden state, IMA Vector LD (2 Loads)
inp_2 = torch.rand (1, in_size)

-- IMA MVM
preact_inp = inp_2 * i2h_mat
preact_h = h_1 * h2h_mat

-- IMA Vector Add
out = preact_inp + preact_h

-- IMA Vector Add
-- out = out + bias_vec

-- IMA Vector Non-Linear operations
i_gate = nl1:forward(out)[{{1}, {0*h_size+1, 0*h_size+h_size}}]
f_gate = nl1:forward(out)[{{1}, {1*h_size+1, 1*h_size+h_size}}]
o_gate = nl1:forward(out)[{{1}, {2*h_size+1, 2*h_size+h_size}}]
c_int = nl2:forward(out)[{{1}, {3*h_size+1, 3*h_size+h_size}}]

-- Update the cell state
-- 2 IMA  Vector multiply & 1 IMA Vector ADD
c_2 = torch.cmul (f_gate, c_1) + torch.cmul (i_gate, c_int)

-- IMA Vector Non-linearity and Vector Multiply
h_2 = torch.cmul (o_gate, nl2:forward(c_2))

print ('Time t+1: ' .. 'Cell state', c_2, 'Hidden state', h_2)

-- save input data, weights and outputs to table
--[[ lstm2 = {}
lstm2['i2h'] = i2h_mat
lstm2['h2h'] = h2h_mat
lstm2['inp1'] = inp_1
lstm2['inp2'] = inp_2
lstm2['h0']   = h_0
lstm2['h1']   = h_1
lstm2['h2']   = h_2
lstm2['c0']   = c_0
lstm2['c1']   = c_1
lstm2['c2']   = c_2

print (lstm2) --]]

-- save table to file
filename = tracepath .. 'lstm.t7'
torch.save (filename, lstm2)

-- save inputs to the input.t7 file for input tile in DPE
inp_path = tracepath .. 'input.t7'
inp = {}
data = torch.ones(2*in_size + 2*h_size)
data[{{1,4}}] = inp_1
data[{{5,7}}] = h_0
data[{{8,10}}] = c_0
data[{{11,14}}] = inp_2
inp['data'] = data
counter = torch.ones(2*in_size + 2*h_size)
inp['counter'] = counter
valid = torch.ones(2*in_size + 2*h_size)
inp['valid'] = valid
print (inp)
torch.save (inp_path, inp)

-- save the weights in the xbar format (tile1 and tile2) for dpe simulations
num_ima = 2
num_xbar = 3
xbar_size = 4

wt_path = tracepath .. 'tile2/weights/'
paths.mkdir (wt_path)

for i = 0,(num_ima-1) do
   for j = 0,(num_xbar-1) do
      temp_path = wt_path .. 'ima' .. i  .. '_xbar' .. j .. '.t7'
      xb_val = torch.zeros(xbar_size, xbar_size)
      if (i == 0) then
         xb_val[{{1,in_size}, {}}] = i2h_mat[{{}, {j*xbar_size+1, (j+1)*xbar_size}}]
      else
         xb_val[{{1,h_size}, {}}] =  h2h_mat[{{}, {j*xbar_size+1, (j+1)*xbar_size}}]
      end
      --print ('xbar_wt_path', temp_path)
      --print ('xbar_wt', xb_val)
      torch.save (temp_path, xb_val)
   end
end

