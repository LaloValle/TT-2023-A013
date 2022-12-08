import time
import pandas as ps
from math import pi,exp
import numpy as np
from Libraries.Tools import standardize
from LLibraries.DTW import DTW, optimal_warping_path

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

def SAX(time_series,number_words:int,alphabet_size:int,numeric_alphabet:bool=True,array_style:bool=False):
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
    return np.array([int(digit) for digit in time_series_string]) if array_style else time_series_string

def SAX_distance(time_series_string_1,time_series_string_2,alphabet_size:int):
    """
        The distance between pairwise elements(a_i,a_k) is:
            0               ->  when their symbols differs at most by one
            b_(k-1) - b_i   ->  when otherwise

        The distance between 2 string is defined as the mean of the pair-wise symbol distances
    """
    # Verifies if the time series strings are alphanumeric
    #   When the difference of the unicode values is between 0 and the alphabet size is an alphanumeric string
    if 0 <= ord(time_series_string_1[0]) - ord('a') <= alphabet_size: time_series_string_1 = alphanumeric_to_numeric(time_series_string_1)
    if 0 <= ord(time_series_string_2[0]) - ord('a') <= alphabet_size: time_series_string_2 = alphanumeric_to_numeric(time_series_string_2)

    pairwise_distances = np.zeros((len(time_series_string_1)))
    breakpoints = equiprobable_breakpoints[str(alphabet_size)]

    for index in range(len(time_series_string_1)):
        digito_1 = int(time_series_string_1[index]); digito_2 = int(time_series_string_2[index])
        difference = abs(digito_1-digito_2)

        if difference > 1: pairwise_distances[index] = breakpoints[max(digito_1,digito_2)-1] - breakpoints[min(digito_1,digito_2)]
    return np.sum(pairwise_distances)

def SAX_DTW_distance(time_series_string_1,time_series_string_2,alphabet_size:int,warping_path:list=[],window_size:int=0):
    # Verifies if the time series strings are alphanumeric
    #   When the difference of the unicode values is between 0 and the alphabet size is an alphanumeric string
    if (type(time_series_string_1) == str) and (0 <= ord(time_series_string_1[0]) - ord('a') <= alphabet_size): time_series_string_1 = alphanumeric_to_numeric(time_series_string_1)
    if (type(time_series_string_2) == str) and (0 <= ord(time_series_string_2[0]) - ord('a') <= alphabet_size): time_series_string_2 = alphanumeric_to_numeric(time_series_string_2)

    pairwise_distances = np.zeros((0),dtype=np.float16)
    breakpoints = equiprobable_breakpoints[str(alphabet_size)]; len_breakpoints = len(breakpoints)

    if not warping_path: warping_path = optimal_warping_path([int(digit) for digit in time_series_string_1] if type(time_series_string_1) == str else time_series_string_1,[int(digit) for digit in time_series_string_2] if type(time_series_string_2) == str else time_series_string_2,window_size=window_size)
    
    for relation in warping_path:
        digito_1 = int(time_series_string_1[relation[0]]); digito_2 = int(time_series_string_2[relation[1]])
        difference = abs(digito_1-digito_2)

        if difference <= 1: pairwise_distances = np.append(pairwise_distances, 0.0)
        elif difference > 1:
            max_index = max(digito_1,digito_2)-1; min_index = min(digito_1,digito_2)
            # Verifies the indexes are inside the range
            if max_index >= len_breakpoints: max_index = len_breakpoints-1
            if min_index < 0: min_index = 0
            pairwise_distances = np.append(pairwise_distances, breakpoints[max_index]-breakpoints[min_index])
    return np.sum(pairwise_distances)

def SAX_DTW_1NN(classification_set:list,training_set:list,alphabet_size:int,window_size:int=0,**kargs):
    predictions=np.array([])
    # Loops through all the sequence to be classified
    for i in range(len(classification_set)):

        classification_series = classification_set[i]
        minimum_distance = float('inf'); closest_sequences_labels = {float('inf'):[]}

        # Loop that calculates the closest sequence of the training set of the current classificaction sequence
        for index_training in range(len(training_set)):
            training_series = training_set[index_training]
            # Computes the SAX-DTW distance
            #   The first termn is excluded as corresponds to the class label value
            distance = SAX_DTW_distance(classification_series[1:],training_series[1:],alphabet_size=alphabet_size,window_size=window_size)
            # Only if the calculated SAX-DTW is smaller than the best current distance
            if distance <= minimum_distance:
                # There is a new smaller distance
                # The closes sequences dictionary gets reseted and saves as the minimum_distance
                if distance != list(closest_sequences_labels.keys())[0]:
                    minimum_distance = distance
                    closest_sequences_labels.clear(); closest_sequences_labels[distance] = list()
                closest_sequences_labels[distance].append(int(training_series[0]))
        # The label value of labels with greater presence is the one assigned for the current classified sequence
        unique_votes,count_votes = np.unique(list(closest_sequences_labels.items())[0][1],return_counts=True)
        predictions = np.append( predictions, int(unique_votes[np.argmax(count_votes)]))

    return predictions



def to_SAX_dataset(dataset,number_words,alphabet_size,numeric_alphabet:bool=True):
    return [np.concatenate(([int(instance[0])], SAX(instance[1:],number_words=number_words,alphabet_size=alphabet_size,numeric_alphabet=numeric_alphabet,array_style=True))) for instance in dataset]

def alphanumeric_to_numeric(time_series_string):
    new_string = ''
    for letter in time_series_string: new_string +=  ord(letter)-ord('a')
    return new_string
    
def numeric_to_alphanumeric(time_series_string):
    new_string = ''
    for letter in time_series_string: new_string +=  ord(letter)-ord('a')
    return new_string