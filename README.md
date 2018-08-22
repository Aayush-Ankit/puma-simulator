# HPE DPE emulator

Below you will find some information on how to use HPE DPE Emulator.

## Table of Contents

- [System requirements](#system-requirements)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Authors](#authors)
- [License](#license)

## System requirements

Below you can find the system requirements and versions tested.

| Requirement | Version                    |
| ----------- | -------------------------- |
| OS: Ubuntu  | 16.04.3 LTS (Xenial Xerus) |
| Python      | 2.7.12                     |

## Quick Start

```sh
sudo apt-get install python-tk

sudo pip install http://download.pytorch.org/whl/cu80/torch-0.3.0.post4-cp27-cp27mu-linux_x86_64.whl

sudo pip install -r <dpe_emulate>/requirements.txt

```

If you are behind a proxy, you should type ```
sudo pip --proxy $http_proxy install ...``` instead.

## Usage

For testing if everything is working fine:

```sh
cd <dpe_emulate>/src

python dpe.py
```
____________________________________________________________
To specify model name and use CSV writer
```sh
python dpe.py --net "mlp(128-2-8)" -xs 128 -nxpc 2 -ncpt 8
```
These values should be entered based on what parameters were set for the compiler before building the model.  

- xs : Crossbar Size  
- nxpc : Number of MVMUs per Core  
- ncpt 8 : Cores per Tile  

Compiled models should be moved to the emulate/test/testasm directory. Outputs and trace of execution folder will be found in /traces
____________________________________________________________

Then, you should see some results like:

```sh
...

('Cycle: ', 8783, 'Tile halt list', [1, 1, 0, 1])
('Cycle: ', 8784, 'Tile halt list', [1, 1, 0, 1])
('Cycle: ', 8785, 'Tile halt list', [1, 1, 0, 1])
('Cycle: ', 8786, 'Tile halt list', [1, 1, 1, 1])
cycle: 8786 Node Halted
Finally node halted | PS: max_cycles 10000
('Dumping tile num: ', 0)
('Dumping tile num: ', 1)
('Dumping tile num: ', 2)
('Dumping tile num: ', 3)
Output Tile dump finished
Success: Hardware results compiled!!
```
## Config.py
- xbar_size must be set to the value used in the compiler (default is 128)  
- num_xbar must be equal to (num_bits/xbar_bits) * MVMUs per Core  
	
	For example: (16/2) * 2 = 16

- num_ima must match the number of cores per tile from the compiler (can also be found by counting the number of core directories in the model)  
- num_tile_compute : this is equal to the number of tiles the model produces minus 2 (since two tiles are set for instructions)  
	
	For example: If the mlp model creates 3 tiles, the value would be 1

- num_tile_max : this value is used to calculate node area and also signifies when the chip-to-chip interconnection will occur (if the model uses  
- more tiles that are able to fit on a node.) Set this value to 138.0 tiles for a comparable value to the DaDianNao accelerator.  

## Authors

TBD

## License

TBD
