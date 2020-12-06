import pandas as pd
import numpy as np

class AlgTester:
    name = 'Tester'
    sample_index = 0
    sampled = False
    sample_sigma = 0
    sample_mu = 0
    window_size = 5

    initial_sample = pd.DataFrame()

    def __init__(self,sigma_thresh=3, initial_sample_size = 1000):
        self.sigma_thresh = sigma_thresh
        self.initial_sample_size = initial_sample_size

    def detect(self,data):
        self.sample_index = self.sample_index + len(data)
        if self.sampled == True:
            for g, df in data.groupby(np.arange(len(data)) // self.window_size):
                if(df.mean()['Resistance'] - self.sample_mu)/self.sample_sigma >= self.sigma_thresh:
                    return 1
                else:
                    return 0
        else:
            self.initial_sample = pd.concat([self.initial_sample, data])
            if(self.sample_index > self.initial_sample_size):
                self.sample_mu = self.initial_sample.mean()['Resistance']
                self.sample_sigma = self.initial_sample.std()['Resistance']
                self.sampled = True
            return -1



