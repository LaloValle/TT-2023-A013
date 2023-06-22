import numpy as np
import matplotlib.pyplot as plt
# Local Modules
from Libraries.DTW import *
from Libraries.Tools import standardize,cross_validation, stratified_sampling
from Libraries.DTWWindowOptimizer import *

def main():
    test_synthetics()


def test_synthetics():
    #===================
    # Series recovering
    #===================
    # Recover a time series from the "Activity Recognition from Single Chest-Mounted Accelerometer" dataset
    # for the first patient in the y axis acceleration for 300 readings only while performing the climbing of stairs
    time_series_1 = np.genfromtxt(
        './Data/1.csv',
        delimiter = ',',
        usecols = (2),          # Reads the values of the 2nd column
        skip_header = 70699,    # Starts the reading in the line 70700
        max_rows = 300          # Reads 300 rows from the starting row
    )
    # Recover a time series from the "Activity Recognition from Single Chest-Mounted Accelerometer" dataset
    # for the first patient in the y axis acceleration for 300 readings only while performing the task of working in the computer
    time_series_2 = np.genfromtxt(
        './Data/1.csv',
        delimiter = ',',
        usecols = (2),          # Reads the values of the 2nd column
        max_rows = 300          # Reads 300 rows from the starting row
    )
    # Standardizing of time_series
    time_series_1 = standardize(time_series_1)
    time_series_2 = standardize(time_series_2)

    #========================
    # Synthethic time series
    #========================
    # The new synthethic time series gets created adding warping and satandarizing it after
    synthetic_time_series = standardize(add_warping(time_series_1))

    #===============
    # DTW distances
    #===============
    #   1. Time series 1 with Synthetic series time from time series 1
    #   2. Time series 1 with Second time series
    dtw_distance_synthetic,_ = DTW(time_series_1, synthetic_time_series)
    dtw_distance_2,_ = DTW(time_series_1, time_series_2)
    print('DTW distance with synthetic time series >> ', dtw_distance_synthetic)
    print('DTW distance between time series >> ', dtw_distance_2)
    
    #==========
    # Plotting
    #==========
    """ fig,axs = plt.subplots(2,1)
    # Comparition of time series 1 with:
    #   1. Synthetic series time from time series 1
    #   2. Second time series
    axs[0].plot([x for x,_ in enumerate(time_series_1)],time_series_1, color='c')
    axs[0].scatter([x for x,_ in enumerate(time_series_1)],time_series_1, color='c')
    axs[0].plot([x for x,_ in enumerate(synthetic_time_series)],synthetic_time_series, color='k')
    axs[0].scatter([x for x,_ in enumerate(synthetic_time_series)],synthetic_time_series, color='k')

    axs[1].plot([x for x,_ in enumerate(time_series_1)],time_series_1, color='c')
    axs[1].scatter([x for x,_ in enumerate(time_series_1)],time_series_1, color='c')
    axs[1].plot([x for x,_ in enumerate(time_series_2)],time_series_2, color='b')
    axs[1].scatter([x for x,_ in enumerate(time_series_2)],time_series_2, color='b') """

    fig,axs = plt.subplots(1)
    # Comparition of time series 1 with:
    #   1. Synthetic series time from time series 1
    #   2. Second time series
    axs.plot([x for x,_ in enumerate(time_series_1)],time_series_1, color='c')
    axs.scatter([x for x,_ in enumerate(time_series_1)],time_series_1, color='c')
    axs.plot([x for x,_ in enumerate(synthetic_time_series)],synthetic_time_series, color='k')
    axs.scatter([x for x,_ in enumerate(synthetic_time_series)],synthetic_time_series, color='k')

    fig.suptitle('Comparación entre una serie de tiempo y su copia sintética')
    fig.supxlabel('Unidades de tiempo')
    fig.supylabel('Aceleraciones en el eje Z')

    plt.show()

def test_10_FCV_DTW_1KNN():
    #===================
    # Series recovering
    #===================
    dataset = np.genfromtxt(
        'Data/train.csv',
        delimiter='\t',
        dtype=np.float16,
        missing_values = {'NaN'},
        filling_values = {np.NaN}
    )
    # Change of position for the first element of the label classes located in the last element in the dataset entries file
    dataset = np.concatenate((dataset[:,-1].reshape((-1,1)),np.delete(dataset,np.s_[-1],axis=1)),axis=1)
    print('Dataset shape >>',dataset.shape)

    # The dataset gets stratified
    stratified_dataset = stratified_sampling(dataset,max_possible_instances=False,instances_per_class=20)
    print('Stratified dataset with 5 instances per class shape >> ', stratified_dataset.shape)
    # Test of the cross validation
    accuracy = cross_validation(stratified_dataset,DTW_1NN,window_size=10)

    # Test of creation of an augmented set with synthetic time series
    new_dataset = create_augmented_set(stratified_dataset,amount_warping=0.2)
    print('New dataset shape >>',new_dataset.shape)
    # Test of the cross validation
    accuracy = cross_validation(new_dataset,DTW_1NN,10)

    # Test of computing the minimum warping window
    window_size = minimum_warping_window(stratified_dataset,DTW_1NN,number_iterations=10,upper_bound_window=10)



if __name__ == '__main__': main()