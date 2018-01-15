-- Record the weights of different nn.Linear layers in the LSTM for xbar
-- currently analysis in dpe_char_rnn

require 'torch'
require 'nn'
require 'nngraph'

require 'util.OneHot'
require 'util.misc'

-- Load checkpoint
cp = torch.load ('cv/lm_lstm_epoch11.82_1.4148.t7_cpu.t7')
num_layers = 2

-- Initialize the data structure to store RNN weights (2*num_layers+1 different
-- tensors)
wt_file = {}

-- Traverse layers
for layer_idx = 1, num_layers do
   for _,node in ipairs(cp.protos.rnn.forwardnodes) do
      if node.data.annotations.name == "i2h_" .. layer_idx then
         -- extract the layer
         wt_file[#wt_file+1] = node.data.module.weight:clone()
         --print (wt_file[#wt_file]:size())
      elseif node.data.annotations.name == "h2h_" .. layer_idx then
         -- extract the layer
         wt_file[#wt_file+1] = node.data.module.weight:clone()
         --print (wt_file[#wt_file]:size())
      elseif layer_idx == num_layers and node.data.annotations.name == "decoder" then
         -- extract the layer
         wt_file[#wt_file+1] = node.data.module.weight:clone()
         --print (wt_file[#wt_file]:size())
      end
   end
end

-- Save wt_file
torch.save('wt_rnn.t7', wt_file)
