# Use dpe_des branch for all designs hereon

# dpe_emulate

## master (designs enlisted in order): (All previous branches present on remote)
### IMA designed and tested
### tile - tile designed (aggregartion of IMAs)
### tile_sync - IMA synchronization added
### tile++ - send/receive/compute instructions added, receive buffer, sned queue added
### node - aggregation of tiles

## master (everything until before - All previous branches merged to master)
### dpe_energyarea - dpe functionality verification with lstm2
### dpe_energyarea - dpe.py wrapper to run DPE on instructions with input data and dump output data
### dpe_vgg - modified ISA (vector instructions for IMA, Tile, control flow instructions for IMA)
### dpe_vgg - runs vgg11(layer1) on DPE and compares energy with Nvidia Quadro K5200
### ima_optim - upadted noc metrics, updated leakage power, debugged metric computation from dpesim
### ima_optim2 - upadted MVM pipeline - 1DAC_array, 1xbInMem, 8xbars

### dpe_charRNN - char-rnn (Karpathy) implemented on DPE
### dpe_des - master merged with dpe_charRNN
### record_xbar - analyze xbar currents for data-optimizations alaysis
### dpe_refine - dpesim after isa_refinements

