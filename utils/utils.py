import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
#Todo make detection time window check
def check_detections(data, detections):
    """
    :param data:
    :param detections:
    :return: results:
        recall
        precision
    """
    true_positives = 0
    false_positives = 0
    false_negatives = 1
    for detection in detections:
        if detection['detection'] > 0:
            if data.loc[detection['time_start']]['Anomaly'] != 0 or data.loc[detection['time_end']]['Anomaly'] != 0:
                #True positive -> detected only anomaly of the dataset
                false_negatives = 0
                true_positives = true_positives + 1
            else:
                #False positive
                false_positives = false_positives + 1
    recall = true_positives/(true_positives + false_negatives)
    precision = true_positives/(true_positives + false_positives)
    results = {
        'recall' : recall,
        'precision':precision
    }
    return results

#Todo calculate precision

#Todo calculate recall

def is_between(index, start, end):
    mask = (index >= start) & (index <= end)

    return mask

#Todo grapher with detections
def plot_graph_detections(data_df,detections):
    data = data_df.resample('1min').mean()
    fig, ax = plt.subplots(figsize=(14,10))
    margin = 5
    ax2 = ax.twinx()
    sns.lineplot(data=data, x="Time", y="Resistance", ax=ax, ci=50,color='red')
    sns.lineplot(data=data, x="Time", y="Frequency", ax=ax2, ci=50, color='blue')
    ax.set_ylim(bottom=np.min(data['Resistance'])-margin, top=np.max(data['Resistance'])+margin)
    ax2.set_ylim(bottom=np.min(data['Frequency'])-margin, top=np.max(data['Frequency'])+margin)
    for detection in detections:
        if detection['detection'] > 0:
            ax.axvspan(detection['time_start'], detection['time_end'], alpha=0.2, color='red')
        else:
            ax.axvspan(detection['time_start'], detection['time_end'], alpha=0.2, color='blue')
    ax.fill_between(data.index, 0, 1, where=data['Anomaly']>0,
                    color='green', alpha=0.2, transform=ax.get_xaxis_transform())
    plt.show()

#Todo grapher with only contamination
def plot_graph_contamination(data_df):
    fig, ax = plt.subplots(figsize=(14,10))
    margin = 5
    ax2 = ax.twinx()
    sns.lineplot(data=data_df, x="Time", y="Resistance", ax=ax, ci=50,color='red')
    sns.lineplot(data=data_df, x="Time", y="Frequency", ax=ax2, ci=50, color='blue')
    ax.set_ylim(bottom=np.min(data_df['Resistance'])-margin, top=np.max(data_df['Resistance'])+margin)
    ax2.set_ylim(bottom=np.min(data_df['Frequency'])-margin, top=np.max(data_df['Frequency'])+margin)
    ax.fill_between(data_df.index, 0, 1, where=data_df['Anomaly']>0,
                    color='green', alpha=0.3, transform=ax.get_xaxis_transform())
    plt.show()
