from glob import glob
import os
import pandas as pd
import numpy as np
from utils.utils import plot_graph_detections,check_detections
import json

class Simulator:
    """"
    Simulator:
    Class that stores values to feed into the detectors from possibly multiple tests stored in the input_folder folder
    with 3 columns: Time, Frequency, Resistance
    the detectors will analyse possible anomalies and return to the simulator
    the simulator will catch the anomalies detected and provide the metrics achieved with it
    there will be a function to test a single algorithm
    there will be a function to test multiple algorithm parameters
    the simulator will save the metrics evaluated
    """
    files_data = []
    data_packet_size = 60
    def __init__(self,input_folder, data_packet_size):
        """
        :param input_folder: Input folder with test csv files
        :param data_packet_size: Size of each iteration
        """
        path_sep = os.path.sep
        if(input_folder[-1]!=path_sep):
            input_folder = input_folder + path_sep
        glob_path = input_folder+'*'
        test_files = glob(glob_path)
        print('{} Tests found'.format(len(test_files)))
        for file in test_files:
            try:
                filename = file.split(path_sep)[-1].split('.')[0]
                data = pd.read_csv(file,sep=',',index_col='Time', parse_dates=['Time'])
                file_data = {
                    'file_name': filename,
                    'file_path': file,
                    'data': data
                }
                self.files_data.append(file_data)
            except BaseException:
                raise(BaseException)
        self.data_packet_size = data_packet_size
        for file in self.files_data:
            print("{}'s data: ".format(file['file_name']))
            print(file['data'].head())
            print(file['data'].describe())
            print('\n\n\n')
    def runDetector(self, algorithm):
        """
        :param algorithm: Algorithm to be tested
        :return: void -> file created in the results folder
            algorithm :
            parameters :
            packet_size:
            results:[
                file_path:
                precision:
                recall:
                detections:
                    time_start:
                    time_end:
                    detection:

            ]
        """
        print('Analysing {} algorithm'.format(algorithm.name))
        results = []
        for file in self.files_data:
            print('Making detections in {} file'.format(file['file_name']))

            data = file['data']
            plot_data = data.resample('1min').mean()
            detections = []
            for g, df in data.groupby(np.arange(len(data)) // self.data_packet_size):
                alg_detection = algorithm.detect(df)
                if alg_detection != 0:
                    detection = {
                        "time_start" : df.index.min(),
                        "time_end" : df.index.max(),
                        "detection" : alg_detection
                    }
                    detections.append(detection)
            detections_result = check_detections(data, detections)
            result = {
                'file_path':file['file_path'],
                'precision':detections_result['precision'],
                'recall':detections_result['recall'],
                'detections':detections
            }
            results.append(result)
            plot_graph_detections(data,detections)
            algorithm.reset()

        alg_result = {
            'algorithm':algorithm.name,
            'parameters':algorithm.get_params(),
            'packet_size': self.data_packet_size,
            'results': results
        }
        out_file_name = './results/{}_{}.json'.format(algorithm.name, algorithm.get_params())
        content = json.dumps(alg_result,indent=4, default=str)
        try:
            with open(out_file_name, 'w') as f:
                f.write(content)
        except Exception as e:
            print(e)
        finally:
            f.close()


