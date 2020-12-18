import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

def plot_simple_stats(data,window_size):
    """
    :param data: dataframe with frequency, resistance and anomaly measurements
    :return:
    """
    bollinger_k = 3
    resistance = data["Resistance"].rolling(window=window_size).mean()
    frequency = data["Frequency"].rolling(window=window_size).mean()

    resistance_std = data["Resistance"].rolling(window=window_size).std()
    frequency_std = data["Frequency"].rolling(window=window_size).std()

    res_upper_bollinger = resistance + resistance_std * bollinger_k
    res_lower_bollinger = resistance - resistance_std * bollinger_k

    freq_upper_bollinger = frequency + frequency_std * bollinger_k
    freq_lower_bollinger = frequency - frequency_std * bollinger_k

    resistance_diff = data["Resistance"].diff().rolling(window=window_size).mean()
    frequency_diff =  data["Frequency"].diff().rolling(window=window_size).mean()
    fig, axs = plt.subplots(2,2, squeeze=True)
    axs[0,0].plot(resistance, alpha=0.7)
    axs[0,0].plot(res_upper_bollinger, alpha=0.2)
    axs[0,0].plot(res_lower_bollinger, alpha=0.2)

    axs[1,0].plot(resistance_diff, alpha=0.7)

    axs[0,1].plot(frequency, alpha=0.7)
    axs[0,1].plot(freq_upper_bollinger, alpha=0.2)
    axs[0,1].plot(freq_lower_bollinger, alpha=0.2)

    axs[1,1].plot(frequency_diff, alpha=0.7)
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()

    fig, axs = plt.subplots(1,2)
    sns.scatterplot(x=resistance, y=frequency,hue=data["Anomaly"], ax=axs[0],alpha=0.3)
    sns.scatterplot(x=resistance_diff, y=frequency_diff,hue=data["Anomaly"],ax=axs[1],alpha=0.3)
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()


