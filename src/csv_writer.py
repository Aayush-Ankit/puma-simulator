import sys
import os
sys.path.insert (0, '/home/michael/hp_dpe/dpe_emulate-br/include/')
import csv
import config as cfg

def write_as_csv(testpath, modelname, mydict, configs):
	# if there is an existing .csv file, read, else make new one 
	#If no inputs, write header and row, else write row
	outputfile = testpath + 'runs.csv'


	mydict['model_name'] = modelname

	#Selected Config Dump
	mydict['xbar_bits'] = cfg.xbar_bits
	mydict['num_xbar'] = cfg.num_xbar
	mydict['xbar_size'] = cfg.xbar_size
	mydict['dataMem_size'] = cfg.dataMem_size
	mydict['instrnMem_size'] = cfg.instrnMem_size
	mydict['num_ima'] = cfg.num_ima
	# mydict['tile_instrnMem_size'] = cfg.tile_instrnMem_size
	# mydict['num_tile_max'] = cfg.num_tile_max
	# mydict['num_node'] = cfg.num_node

	#Passed configs
	mydict['XBAR_SIZE'] = configs[0]
	mydict['N_XBARS_PER_CORE'] = configs[1]
	mydict['N_CORES_PER_TILE'] = configs[2]
	mydict['MAX_LOAD_STORE_WIDTH'] = configs[3]
	mydict['MAX_SET_RECV_WIDTH'] = configs[4]
	mydict['DATA_MEM_PER_CORE'] = configs[5]

	fieldnames = ['model_name','leakage_energy(J)','dynamic_energy(J)','total_energy(J)',
                'leakage_power(mW)','average_power(mW)','peak_power(mW)',
                'node_area(mm^2)','tile_area(mm^2)','core_area(mm^2)',
                'cycles','time(sec)','network_packet_inj_rate','num_tiles','xbar_bits',
				'num_xbar','xbar_size','dataMem_size','instrnMem_size','num_ima',
				'XBAR_SIZE','N_XBARS_PER_CORE','N_CORES_PER_TILE','MAX_LOAD_STORE_WIDTH',
				'MAX_SET_RECV_WIDTH','DATA_MEM_PER_CORE']

	outputfile = testpath + 'runs.csv'
	if os.path.isfile(outputfile):
		print("Appending to runs file")
		with open(outputfile, 'a') as csv_file:
			w = csv.DictWriter(csv_file, fieldnames=fieldnames)
			w.writerow(mydict)
	else:
		print("Making runs file")
		with open(outputfile, 'wb') as csv_file:
			w = csv.DictWriter(csv_file, fieldnames=fieldnames)
			w.writeheader() #If no inputs, write header and row, else write row
			w.writerow(mydict)
	print("Wrote CSV File!")
##Maybe add more methods for manipulation of csv runs reading etc
