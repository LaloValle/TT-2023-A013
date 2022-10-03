import time
import random
import resampy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from LLibraries.DTW import DTW
from LLibraries.Tools import accuracy, cross_validation

#---------
# Resampy
#---------
# https://resampy.readthedocs.io/en/master/example.html

def add_warping(time_series,amount_warping:float=0.20,convert_int:bool=False):
    """
    1. Nolinearly shrink of the time serie by removing randomly data points up to a 80%
        of the original length
    2. Adding of padding by repeating 10 times the endpoints values
    3. The new synthetic series gets resampled to the original length of the series + the added padding
    4. The endpoints get trimmed again
    """
    len_time_series = len(time_series)
    if convert_int: time_series = time_series.astype(np.float32)

    # Nonlinear shrink
    delete_indexes = np.random.permutation(len_time_series)[:int(len_time_series*amount_warping)]
    warped_time_series = np.delete(time_series, delete_indexes)

    # Adding padding
    #   Adds 10% of padding elements, bound to a maximum of 15 elements
    padding_elements = int(len_time_series*.10) if len_time_series < 150 else 15
    warped_time_series = np.concatenate((
        warped_time_series[:padding_elements][::-1],  # Head padding
        warped_time_series,
        warped_time_series[-padding_elements:][::-1] # Tail padding
    ))

    # Resampling
    warped_time_series = resampy.resample(warped_time_series, len(warped_time_series), len_time_series+(2*padding_elements))

    # Trimmed of endpoints
    warped_time_series = warped_time_series[padding_elements:len_time_series+padding_elements]

    if convert_int: 
        warped_time_series = np.rint(warped_time_series)
        list_unique = list(np.unique(warped_time_series))
        if (-0 in list_unique) or (8 in list_unique):
            # Hard coded the upper limit of the alphabet to 7 simbols
            warped_time_series[warped_time_series <= 0] = 0
            warped_time_series[warped_time_series > 7] = 7

    return warped_time_series

def create_augmented_set(time_series_set,amount_warping:float=0.20,percentaje_real_objects:float=0.2,convert_int:bool=False):
    # The original time series set gets split into the objects that will remain as the original and those that will be warped
    # to create a set of synthetic. Is randomly shuffle before making the split
    shuffled_time_series_set = list(time_series_set)
    random.shuffle(shuffled_time_series_set)
    real_time_series, synthetic_time_series = shuffled_time_series_set[:int(len(time_series_set)*percentaje_real_objects)],shuffled_time_series_set[int(len(time_series_set)*percentaje_real_objects):]
    
    # Adds warping to each time series in the set
    for index_synthetic in range(len(synthetic_time_series)):
        # Adds the warping to the actual time series with index index_synthetic and as first element adds the class label
        synthetic_time_series[index_synthetic] = np.concatenate(([synthetic_time_series[index_synthetic][0]],add_warping(synthetic_time_series[index_synthetic][1:],amount_warping=amount_warping,convert_int=convert_int)))
        if convert_int: synthetic_time_series[index_synthetic] = synthetic_time_series[index_synthetic].astype(np.int8)
    
    return real_time_series + synthetic_time_series

def minimum_warping_window(time_series_set,prediction_function,alphabet_size:int=0,number_iterations:int=10,upper_bound_window:int=0,lower_bound_window:int=2,representatives:dict=dict(),convert_int:bool=False,verbose:bool=False,k=10):
    window_sizes_range = range(lower_bound_window, time_series_set[0].size if not upper_bound_window else upper_bound_window+1)[::-1]
    # The number of rows corresponds to the number for iterations
    # and each column to a window size
    WindowSize_vs_Accuracy = np.zeros((number_iterations,window_sizes_range[0]-(lower_bound_window-1)))
    total_time_perfomed = time.time()

    print('\n\n<=== Minimum warping window with a total of {} iterations in a dataset of length {} ===>'.format(number_iterations,len(time_series_set)))

    for iteration in range(number_iterations):
        # Create a new time series set with synthetic and original instances
        starting_time = time.time()
        new_time_series_set = create_augmented_set(time_series_set,convert_int=convert_int)
        # print('Synthetic instance example >> ', new_time_series_set[-1])
        if verbose: print('\n<=== Starting iteration #{} ===>'.format(iteration))

        # Window size from the largest time series size as upper bound and 2 as lower bound, tipically
        for window in window_sizes_range:
            # The accuracy with the actual window and iteration gets saved in the row with row index=iteration and
            # column with index column=window-1 of the WindowSize_vs_Accuracy array
            accuracy = cross_validation(new_time_series_set,prediction_function,window_size=window,alphabet_size=alphabet_size,representatives=representatives,k=k)
            WindowSize_vs_Accuracy[iteration,window-lower_bound_window] = accuracy
            print('window >> ',window,' accuracy >> ', accuracy)
            if verbose: print('<--- iteration:{}, window:{}, accuracy:{:.2f} --->'.format(iteration,window,accuracy))

        finishing_time = time.time()-starting_time
        total_time_perfomed += finishing_time
        print('\n<=== Iteration #{} finished in {:.2f} sec ===>\n'.format(iteration,finishing_time))
    
    # In the final row the mean accuracy for each column(window size) through the k number of iterations is added
    WindowSize_vs_Accuracy = np.concatenate((WindowSize_vs_Accuracy,np.mean(WindowSize_vs_Accuracy,axis=0).reshape(1,-1))) 
    table_WindowSize_vs_Accuracy = pd.DataFrame(WindowSize_vs_Accuracy)
    # Saves the array
    table_WindowSize_vs_Accuracy.to_csv('Results/WindowSize_vs_Accuracy.csv')
    print('\n',table_WindowSize_vs_Accuracy)

    # The index of the column(window size) with the maximum value for the accuracy mean computed in the last row
    # is the best value for the window width in the DTW algorithm
    best_window_width = np.argmax(WindowSize_vs_Accuracy[-1]) + lower_bound_window
    print('\n<=== Minimum warping window ended with a total of {:.2f} sec and a best window width of {} ===>'.format(total_time_perfomed,best_window_width))
    return best_window_width

