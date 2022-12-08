import time
import random
import numpy as np
import pandas as ps

def euclidean_distance(x,y):
    return (x-y)**2


def standardize(dataset):
    """ Standardize a data vector such that scales all the values
    to a mean of 0 and a standard deviation of 1

    Parameters
    ----------
    dataset : list of arrays
        List of multiple arrays
    
    Returns
    -------
    standardize_dataset : list
        List of arrays standardized so that the values met the mean
        of 0 and standard deviation of a normal distribution
    """
    for index in range(len(dataset)):
        dataset[index] = (dataset[index] - np.mean(dataset[index])) / np.std(dataset[index])
    return dataset

def accuracy(test_labels,predictions):
    return (test_labels == predictions).sum()/len(test_labels)




def add_label_column(dataset,class_instances):
    for index in range(len(dataset)):
        dataset[index] = np.insert(dataset[index],0,class_instances[index])
    return dataset

def to_list_time_series_dataset(time_series_dataset):
    list_dataset = []
    
    for time_series in time_series_dataset:
        # Removes the elements of the array that are NaN
        list_dataset.append(np.delete(time_series, np.isnan(time_series)))

    return list_dataset




def cross_validation(time_series_set,prediction_function,window_size:int=0,alphabet_size:int=0,k:int=10,representatives:dict=dict(),verbose:bool=False):
    # Previous configurations and variables
    aux_time_series_set = list(time_series_set); random.shuffle(aux_time_series_set)
    accuracy_log = np.zeros((k))
    training_set_size = int(len(time_series_set)/k)
    total_time_performed = 0

    if verbose: print('\n<=== Starting {}-Fold Cross Validation ===>'.format(k))

    # Loops through the k iterations of the k-folds
    for i in range(k):
        training_set,testing_set = [],[]
        starting_time = time.time()

        if verbose: print('\n<--- Starting K-fold with k={} --->'.format(i))
        # When is the last k the sets are conformed so that the test
        # set remains with the same size in all iterations
        if i == (k-1): 
            testing_set = aux_time_series_set[-training_set_size:]
            training_set = aux_time_series_set[:-training_set_size]
        # When k is not in the last iteration
        else:
            testing_set = aux_time_series_set[i*training_set_size:(i+1)*training_set_size]
            training_set = aux_time_series_set[:i*training_set_size] + aux_time_series_set[(i+1)*training_set_size:]

        # Performs the prediction of the test set
        predictions = prediction_function(testing_set,training_set,window_size=window_size,alphabet_size=alphabet_size,representatives=representatives)
        # The label class is the first element of the series
        test_labels = np.array([instance[0] for instance in testing_set],dtype=np.ubyte)
        acc = accuracy(test_labels,predictions)
        accuracy_log[i] = acc

        ending_time = time.time()-starting_time
        total_time_performed += ending_time
        if verbose: print('<--- Prediction perfomed in {}sec, accuracy: {}% --->'.format(ending_time,acc))
    
    if verbose: print('Accuracy log >> ',ps.DataFrame(accuracy_log))
    print('<=== CV finished. Time : {:.4f} sec, mean accuracy : {:.2f}% ===>'.format(total_time_performed,accuracy_log.mean()*100))
    return accuracy_log.mean()

def stratified_sampling(dataset,max_possible_instances:bool=True,instances_per_class:int=20) -> list:
    class_labels,count_classes = np.unique(dataset[:,0],return_counts=True)

    # Finds the maximum possible instances per class such that every class has the same number of instances in the new dataset
    if max_possible_instances: instances_per_class = min(count_classes)
    # Verifies the value of the instances_per_classes parameter is possible given the number of instances in the dataset
    elif min(count_classes) < instances_per_class: instances_per_class = min(count_classes)

    # The class labels gets transformed into a dictionary. It's used to count
    # the number of instances already added to the final dataset per class
    class_labels = { int(label):instances_per_class for label in class_labels }
    # Creation of the new dataset
    stratified_dataset = np.empty((instances_per_class*len(class_labels), dataset.shape[1]))
    aux_dataset = np.copy(dataset); np.random.shuffle(aux_dataset)
    instance_index = 0; stratified_index = 0

    # Loops until no more class labels are left in the class_labels dictionary
    #   - Every time an instance of a class gets added to the final dataset the count in the entry for
    #     the class in the class_label dictionary gets substracted by one
    #   - Every time the number of instance per class dropdowns to zero the entry in the dictionary 
    #     gets removed from the structure
    while class_labels:
        stratified_dataset[stratified_index] = np.copy(aux_dataset[instance_index])

        actual_class = int(aux_dataset[instance_index,0])
        if actual_class in class_labels.keys(): 
            class_labels[actual_class] -= 1
            stratified_index += 1
            # There's 0 instances left to add
            if class_labels[actual_class] == 0: del class_labels[actual_class]

        instance_index += 1

    return to_list_time_series_dataset(stratified_dataset)

def group_by_class(dataset,with_class_label:bool=False):
    """Splits and groups the instances of a time series dataset in its respective class labels

    Parameters
    ----------
    dataset : list
        List of arrays that represents the time series

    with_class_label : bool
        Determines if the arrays in the dictionary are returned with the class label as first element, otherwise the class
        label is removed from the time series
    
    Returns
    -------
    dataset_by_classes : dict
        Dictionary with labels values as keys and a list of time series as value.
        If time series is returned with or without the label class at the beginning depends of the parameter with_class_label
    """
    dataset_by_classes = dict()

    for index in range(len(dataset)):
        label = int(dataset[index][0])

        if label not in list(dataset_by_classes.keys()):
            dataset_by_classes[label] = list()
        dataset_by_classes[label].append(dataset[index][int(not with_class_label):])
    
    return dataset_by_classes