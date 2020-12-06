from glob import glob
import os
import pandas as pd
import numpy as np

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
                data = pd.read_csv(file,sep=',')
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
        """
        print('Analysing {} algorithm'.format(algorithm.name))
        for file in self.files_data:
            print('Making detections in {} file'.format(file['file_name']))

            data = file['data']
            for g, df in data.groupby(np.arange(len(data)) // self.data_packet_size):
                algorithm.detect(df)

                # print(df.shape)

