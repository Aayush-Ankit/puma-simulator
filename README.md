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
Success: Hadrware results compiled!!
```

## Authors

TBD

## License

TBD
