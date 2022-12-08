import numpy as np
from math import sqrt
from Libraries.Tools import euclidean_distance

#
#-----
# PYS
#-----
# https://pyts.readthedocs.io/en/stable/index.html
#
# http://alexminnaar.com/2014/04/16/Time-Series-Classification-and-Clustering-with-Python.html
# 

def DTW(series_1, series_2, window_size:int=0, distance=euclidean_distance, compute_path:bool=False):
    """Dynamic Time Warping finds an optimal non-linear aligmente between 2 time series(series_1,series_2)

    Parameters
    ----------
    series_1 : list
        First time series

    series_2 : list
        Second time series
    
    window_size : int
        Size of the main diagonal size.
        This constrained is used to speed up the compute of the cost matrix as well as providing a more acurate optimal path when choose correctly

    distance : function
        Distance function to compute the cost between elements of the series

    compute_path : bool
        Flag used to indicate if the optimal warping path must be calculated or not
    
    Returns
    -------
    optimal_warping_path : float
        The total cost of the optimal warping path between the given time series
    
    path : list
        Path of the optimal warping for the elements of the series
    """
    # Chooses the value of the window size
    #   When a value for the window is not given:
    #       Chooses the maximum length between the both series
    if not window_size : window_size = max(len(series_1),len(series_2))

    # Defines the cost matrix with a padding
    #   The size of the matrix is:
    #       (n+1)x(m+1)
    #       where n and m are the size of the series series_1 and series_2 respectively
    DTW = np.full((len(series_1)+1,len(series_2)+1),9999999.99)
    # The padding of the cost matrix gets filled with 0's
    DTW[0,0] = 0


    # Loops for computing the cost between each elements of the series
    #   This first loops between the elements of the series_1 time series
    for i in range(1,len(series_1)+1):
        # This second loops between the elements of the series_2 time series
        #   The window size constrained gets applied in the indexes of the second series
        for j in range(max(0, i-window_size)+1, min(len(series_2), i+window_size)+1):
            cost = distance(series_1[i-1],series_2[j-1])
            DTW[i][j] = cost + min(DTW[i-1][j],DTW[i][j-1],DTW[i-1][j-1])

    # Back tracking of the optimal path follow
    path = [(len(series_1)-1,len(series_2)-1)]; i = len(series_1); j = min(len(series_2), i+window_size)
    while compute_path:
        # The costs of the prior neighbours cells gets sorted
        costs_neighbours_sorted = np.array([DTW[i-1][j],DTW[i-1][j-1],DTW[i][j-1]]).argsort()
        # Depending of the index sorted as first the window gets moved in the first, second, of both axis
        if costs_neighbours_sorted[0] == 0: i -= 1
        elif costs_neighbours_sorted[0] == 1: i -= 1; j -= 1
        elif costs_neighbours_sorted[0] == 2: j -= 1
        
        # When reaching in any axis to the first element the back tracking is complete
        if not i or not j: break
        # The coordinate pair gets added to the path
        path.append((i-1,j-1))


    return sqrt(DTW[len(series_1)][len(series_2)]), path[::-1]

def LB_Keogh(series_1,series_2,r):
    LB_sum=0
    for index,value in enumerate(series_1):

        lower_bound=min(series_2[(index-r if index-r>=0 else 0):(index+r)])
        upper_bound=max(series_2[(index-r if index-r>=0 else 0):(index+r)])

        if value>upper_bound:
            LB_sum=LB_sum+(value-upper_bound)**2
        elif value<lower_bound:
            LB_sum=LB_sum+(value-lower_bound)**2

    return sqrt(LB_sum)


def DTW_1NN(classification_set:list,training_set:list,window_size:int=0,lb_keogh_r:int=5):
    """ KNN with K equals to 1 that in contrast with most implementations uses the
    DTW distance as distance function between sequences
    
    Parameters
    ----------
    classification_set : list
        List of the sequences to be classified
    
    training_set : list
        List of the sequences used as training set

    window_size : int
        Size of the Sakoe-Chiba band for the DTW distance compute
        By default it's 0, meaning the maximum value of the window
    
    lb_keogh_r : int
        Size of the parameter for the LB Keogh lower bound
    
    Returns
    -------
    classification_report :
        Returns a simple report of the sequences classified by comparing the actual label of the sequence
        with the predicted one by the DTW-1NN algorithm

    predictions : list
        List of the predicted labels for each clasification sequence
    """
    predictions=[]; dtw_calculated = 0
    # Loops through all the sequence to be classified
    for i in range(len(classification_set)):

        classification_series = classification_set[i]
        minimum_distance = float('inf'); closest_sequence_label=-1

        # Loop that calculates the closest sequence of the training set of the current classificaction sequence
        for training_series in training_set:
            # Verifies the LB Keogh lower bound is less than the last minimum distance
            #   As the LB Keogh lower bound is less or equal to the DTW distance and
            #   is used to discriminate sequences that are not that similar to the
            #   current to-be-classified sequence but with a linear complexity instead
            #   of the cuadratic of DTW
            if LB_Keogh(classification_series[1:],training_series[1:],lb_keogh_r) < minimum_distance:
                # Computes the actual DTW distance
                #   The last termn is excluded as corresponds to the class label value
                distance,_ = DTW(classification_series[1:],training_series[1:],window_size)
                dtw_calculated += 1
                # Only if the calculated DTW is smaller than the best current distance
                if distance < minimum_distance:
                    minimum_distance = distance; closest_sequence_label = training_series[0]
        # The label value of the closest secuence in the training set is the assigned for the current classified sequence
        predictions.append(int(closest_sequence_label))

    # print('Predictions >> ', predictions)
    # print('Training set >> ', classification_set[:,0].astype(np.ubyte))
    #print('DTW calculated >> {} times'.format(dtw_calculated))
    return predictions
