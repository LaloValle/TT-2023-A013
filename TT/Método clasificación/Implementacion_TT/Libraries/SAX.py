import time
from math import pi,exp
import numpy as np
from Libraries.Tools import standardize

#-------------
#   Tslearn
#-------------
# A ML toolkit dedicated to time-series data
# https://pypi.org/project/tslearn/
#
#
# https://github.com/nphoff/saxpy/blob/master/saxpy.py
#

# The breakpoints divides equiprobable the space for the alfabet assignation taking in count
# a standar normal distribution tendency from the data in the time series
equiprobable_breakpoints = { 
    '3' : [-0.43, 0.43],
    '4' : [-0.67, 0, 0.67],
    '5' : [-0.84, -0.25, 0.25, 0.84],
    '6' : [-0.97, -0.43, 0, 0.43, 0.97],
    '7' : [-1.07, -0.57, -0.18, 0.18, 0.57, 1.07],
    '8' : [-1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15],
    '9' : [-1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22],
    '10': [-1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28],
    '11': [-1.34, -0.91, -0.6, -0.35, -0.11, 0.11, 0.35, 0.6, 0.91, 1.34],
    '12': [-1.38, -0.97, -0.67, -0.43, -0.21, 0, 0.21, 0.43, 0.67, 0.97, 1.38],
    '13': [-1.43, -1.02, -0.74, -0.5, -0.29, -0.1, 0.1, 0.29, 0.5, 0.74, 1.02, 1.43],
    '14': [-1.47, -1.07, -0.79, -0.57, -0.37, -0.18, 0, 0.18, 0.37, 0.57, 0.79, 1.07, 1.47],
    '15': [-1.5, -1.11, -0.84, -0.62, -0.43, -0.25, -0.08, 0.08, 0.25, 0.43, 0.62, 0.84, 1.11, 1.5],
    '16': [-1.53, -1.15, -0.89, -0.67, -0.49, -0.32, -0.16, 0, 0.16, 0.32, 0.49, 0.67, 0.89, 1.15, 1.53],
    '17': [-1.56, -1.19, -0.93, -0.72, -0.54, -0.38, -0.22, -0.07, 0.07, 0.22, 0.38, 0.54, 0.72, 0.93, 1.19, 1.56],
    '18': [-1.59, -1.22, -0.97, -0.76, -0.59, -0.43, -0.28, -0.14, 0, 0.14, 0.28, 0.43, 0.59, 0.76, 0.97, 1.22, 1.59],
    '19': [-1.62, -1.25, -1, -0.8, -0.63, -0.48, -0.34, -0.2, -0.07, 0.07, 0.2, 0.34, 0.48, 0.63, 0.8, 1, 1.25, 1.62],
    '20': [-1.64, -1.28, -1.04, -0.84, -0.67, -0.52, -0.39, -0.25, -0.13, 0, 0.13, 0.25, 0.39, 0.52, 0.67, 0.84, 1.04, 1.28, 1.64]
}

# 
# https://vigne.sh/posts/piecewise-aggregate-approx/
#

def PAA(time_series,intervals:int):
    time_series_length = len(time_series)
    #
    #   Base cases
    #
    # Same number of intervals as the elements in the series
    if time_series_length == intervals: return time_series
    # One interval equals to the mean of the whole series
    if intervals == 1: return np.mean(time_series)
    # Verifies the number of intervals is smaller than the lenght of the time series
    if time_series_length < intervals: return False

    # When the number of intervals is a multiple of the time series length
    # a simple equally split of the time series is perfomed
    if (time_series_length % intervals) == 0:
        # The new approximate time series gets splited into equally distributed intervals of rows
        aproximate_time_series = time_series.reshape((intervals,-1))
        return np.mean(aproximate_time_series,axis=1)
    # When the number of intervals cannot be achieved whit an equally-sized partition of the time series
    # the frame must be resized to obtain an equi-sized
    if time_series_length % intervals:
        #=============
        # First method
        #=============
        #
        # Time : 0.00015115737915039062 sec
        #
        """ value_space = np.arange(0, time_series_length*intervals)
        # Vector that represents the index of the input_index array
        output_index = value_space // time_series_length
        # Vector that represents the index of the values of the original time series that will be used to
        # compute the mean of the resultant time series for each interval
        input_index = value_space // intervals
        print('Space >>',value_space)
        print('Output >>',output_index)
        print('Input >>',input_index)
        uniques, counts_uniques = np.unique(output_index, return_counts=True)
        print('Uniques >>',uniques)
        print('Counts >>',counts_uniques)
        print('Counts cumsum >>',counts_uniques.cumsum())
        print('Split >>',np.split(input_index, counts_uniques.cumsum()))
        result = [time_series[indices].sum() / time_series.shape[0] for indices in np.split(input_index, counts_uniques.cumsum())[:-1]] """

        #==============
        # Second method
        #==============
        #
        # Time : 8.130073547363281e-05
        # ******* Best option ********
        #
        # Array with the indexes that will be used for the compute of the mean of the number of intervals specified
        indexes = ((np.arange(0, time_series_length*intervals)) // intervals).reshape((intervals,-1))
        # Obtains the values of the indexes specified in the indexes array and computes the mean of each row
        return np.mean(np.array([ [ time_series[index] for index in row ] for row in indexes]),axis=1)

def SAX(time_series,number_words:int,alphabet_size:int,numeric_alphabet:bool=True):
    # Initialization of variables
    breakpoints = equiprobable_breakpoints[str(alphabet_size)]
    time_series_string = ''

    # First the time series get discretized with PAA after being standardize
    discrete_time_series = PAA(standardize(time_series),number_words)

    # Loops through the discretized points of the time series
    for word in discrete_time_series:
        word_found = False

        # Loop through the bounds defined by each breakpoint
        for bound_index in range(len(breakpoints)):
            # When the value of the discrete word is less or equal
            # to the breakpoint bound belongs to the actual index character
            if word <= breakpoints[bound_index]:
                time_series_string += str(bound_index) if numeric_alphabet else chr(ord('a') + bound_index)
                word_found = True
                break
        
        # Belong to the upper bound of the breakpoints available
        # therefore the last character of the alphabet
        if not word_found: time_series_string += str(len(breakpoints)) if numeric_alphabet else chr(ord('a') + len(breakpoints))
    return time_series_string