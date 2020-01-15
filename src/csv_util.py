import csv
def hw_stats_metric_to_csv_file(metric_dict, file_name):
    
    with open(file_name, 'wb') as csv_file:
        writer = csv.DictWriter(csv_file, metric_dict.keys())
        writer.writeheader()
        writer.writerow(metric_dict)

if __name__ == "__main__":

    metric_dict = {
        'neural_network': '',
        'num_tiles': 0, 
        'leakage_energy':0.0,
        'dynamic_energy':0.0,
        'total_energy':0.0,
        'average_power':0.0,
        'peak_power':0.0,
        'leakage_power':0.0,
        'node_area':0.0,
        'tile_area':0.0,
        'core_area':0.0,
        'cycles':0,
        'time':0.0}

    metric_dict['neural_network'] = 'MLP 2'
    metric_dict['num_tiles'] = 7
    metric_dict['leakage_energy'] =  9.14912388058e-07
    metric_dict['dynamic_energy'] = 1.23312997142e-06
    metric_dict['total_energy'] = 2.14804235948e-06
    metric_dict['average_power'] = 236.256308785
    metric_dict['peak_power'] = 1458.99749907
    metric_dict['leakage_power'] = 193.533145093
    metric_dict['node_area'] = 110.887419603
    metric_dict['tile_area'] = 0.512103688115
    metric_dict['core_area'] = 0.0382013232115
    metric_dict['cycles'] = 9092
    metric_dict['time'] = 9.092e-06
    

    print(metric_dict)

    hw_stats_metric_to_csv_file (metric_dict)