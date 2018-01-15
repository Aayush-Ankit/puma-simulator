require 'nn'
require 'nngraph'
require 'cunn'
require 'cutorch'

LSTM = require 'LSTM.lua'

in_size = 65
rnn_size = 128
-- 3-layer LSTM network (input and output have in_size dimensions)
network = {LSTM.create(in_size, rnn_size):cuda(), LSTM.create(rnn_size, rnn_size):cuda(), LSTM.create(rnn_size, in_size):cuda()}

-- network input
x = torch.randn(1, in_size):cuda()
previous_state = {
  {torch.zeros(1, rnn_size):cuda(), torch.zeros(1,in_size):cuda()},
  {torch.zeros(1, rnn_size):cuda(), torch.zeros(1,rnn_size):cuda()},
  {torch.zeros(1, rnn_size):cuda(), torch.zeros(1,in_size):cuda()}
}

-- network output
output = nil
next_state = {}

-- forward pass
layer_input = {x, table.unpack(previous_state[1])}
for l = 1, #network do
  -- forward the input
  layer_output = network[l]:forward(layer_input)
  -- save output state for next iteration
  table.insert(next_state, layer_output)
  -- extract hidden state from output
  layer_h = layer_output[2]
  -- prepare next layer's input or set the output
  if l < #network then
    layer_input = {layer_h, table.unpack(previous_state[l + 1])}
  else
    output = layer_h
  end
end

print(next_state)
print(output)
