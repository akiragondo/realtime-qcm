import numpy as np
import pandas as pd


class AlgTester:
    name = 'Simple Change Detector'
    sample = pd.DataFrame()
    last_sample_avg = 0
    diff_thresh = 0
    change_detected = False
    constant_change_detected = False

    def __init__(self, window_size = 600, sigma_thresh = 6, constant_change_thresh = 1, response_time = 15):
        """
        :param window_size: Window of analysis for the change difference detection
        :param sigma_thresh: How many standard deviations the derivative must exceed for the detection to be made
        :param constant_change_thresh: Percentage points the system window needs to deviate for it to be considered an anomaly
        :param response_time:
            - Experimentally - constant_change has never been below 1 for any concentration
            - Sigma_thresh - values between 3 and 6 are expectedly good
            - Window size - changes how slow or quick the anomalies are expected to be -> smalled window sizes can detect
             faster anomalies and larger ones can detect slower deviations
        """
        self.window_size = window_size
        self.sigma_thresh = sigma_thresh
        self.constant_change_thresh = constant_change_thresh

    def get_params(self):
        """
        :return: String with parameters, separated by semi-colons
        """
        return "window_size={};sigma_thresh={};constant_change_thresh={}".format(
            self.window_size,
            self.window_size,
            self.constant_change_thresh
        )

    def reset(self):
        self.last_sample_avg = 0
        self.change_detected = False
        self.constant_change_detected = False
        self.sample = pd.DataFrame()

    def detect(self,data):





