import sys
import os
import numpy
import argparse

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, root_dir)

test_dir = os.path.join(root_dir, "test")
sys.path.insert(0, test_dir)

trace_dir = os.path.join(root_dir, "test/traces")
sys.path.insert(0, trace_dir)

sys.path.insert(0, os.path.join(root_dir, "include"))
sys.path.insert(0, os.path.join(root_dir, "src"))

from src.data_convert import *
import src.ima as ima
from src.instrn_proto import *
import include.config as cfg


class RegTest1:

    def run(self, net):
        print("Trace directory: ", trace_dir)
        net_dir = os.path.join(trace_dir, str(net))
        weight_dir = os.path.join(root_dir, "test/testasm/" + str(net) + "/weights")
        sys.path.insert(0, net_dir)
        sys.path.insert(0, weight_dir)
        print("Net directory: ", net_dir)
        print(" Weight  directory: ", weight_dir)

        assert (os.path.exists(net_dir) ==1), 'Could not find net'
        '''if not os.path.exists(net_dir):
            os.makedirs(net_dir)
            for i in range (cfg.num_tile):
                temp_tiledir = net_dir +'/tile' + str(i)
                os.makedirs(temp_tiledir)'''
              
        avg_mean_err = 0.0
        avg_stdev_err = 0.0
        count = 1

        for i in range(cfg.num_tile):
            memsim_file = trace_dir + '/' + str(net) + '/tile' + str(i) + '/memsim.txt'
            #print(memsim_file)
            assert(os.path.exists(memsim_file)), 'Could not find memsim dump. Please run src/dpe.py first.'
            for j in range (cfg.num_ima):
                #print('Tile' + str(i) + ' , Core ' + str(j) + '\n')
                for k in range (cfg.num_matrix):
                    weight_file = weight_dir + '/tile' + str(i) + '/core' + str(j) + '/log_xbar' + str(k) +'.npy'
                    if (os.path.exists(weight_file)):
                        weights = np.float64(np.load(weight_file))
                        assert(weights.shape == (cfg.xbar_size, cfg.xbar_size)), 'Weights should have same size as Xbar'
                    else:
                        weights = np.zeros((cfg.xbar_size, cfg.xbar_size))
                    with open(memsim_file) as f:
                        line = []
                        l = f.readlines()
                        for ii in l:
                            t = ii.strip()
                            line.append(t)
                            
                        ip =  'Xbar Input Memory: CoreId: ' + str(j) + ' matrixId: ' + str(k) + ' mvmu_type: f  contents' 
                        op =  'Xbar Output Memory: CoreId: ' + str(j) + ' matrixId: ' + str(k) + ' mvmu_type: f  contents'
                        #print(ip)
                        if ip in line and  not (len(line[line.index(ip)+1:line.index(op)]) < cfg.xbar_size):
                            inputs = np.asarray(line[line.index(ip)+1: line.index(ip) + cfg.xbar_size + 1]).astype(np.float)
                            #print(inputs)
                        else:
                            inputs = np.zeros((cfg.xbar_size,1))
                            
                        #op =  'Xbar Output Memory: CoreId: ' + str(j) + ' matrixId: ' + str(k) + ' mvmu_type: f  contents'
                        #print(op)
                        if op in line and 'Xbar' not in line[line.index(ip)+1]:
                            out_exp = np.asarray(line[line.index(op)+1: line.index(op) + cfg.xbar_size + 1]).astype(np.float)
                            #print(out_exp)
                        else:
                            out_exp = np.zeros((cfg.xbar_size,1))
                        out_gold = np.dot(weights,inputs)

                        err = np.tanh(out_gold) - np.tanh(out_exp)

                        print("error for Tile " + str(i) + " , Core " + str(j) + " , Matrix " + str(k) + " has mean " + str(np.average(err)) + " and stdev " + str(np.std(err))) 
                        
                        avg_mean_err += np.average(err)
                        avg_stdev_err += np.std(err)
                        count += 1
             
        avg_mean_err = avg_mean_err/count
        avg_stdev_err = avg_stdev_err/count

    
        print("On average, for all tiles, error has mean " + str(avg_mean_err) + " and stdev " + str(avg_stdev_err))    





                





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-n", "--net", help="The net name as it is in test/traces")
    args = parser.parse_args()
    net = args.net

    print('Running Regression Test 1 for {} \n'.format(net))
    RegTest1().run(net) 
    



