import time
import numpy as np

def euclidean_distance(x,y):
    return (x-y)**2

def standardize(vector):
    """ Standardize a data vector such that scales all the values
    to a mean of 0 and a standard deviation of 1

    Parameters
    ----------
    vector : array
        Array of 1-D
    
    Returns
    -------
    standardize_vector : array
        Arrays standardize so that the values met the mean of 0 and
        standard deviation of a normal distribution
    """
    return (vector - np.mean(vector)) / np.std(vector)

def accuracy(test_labels,predictions):
    return (test_labels == predictions).sum()/len(test_labels)




def add_class_column(dataset,class_instances):
    return np.concatenate((class_instances.reshape((-1,1)),dataset),axis=1)






def cross_validation(time_series_set,prediction_function,window_size:int=0,k:int=10,verbose:bool=False):
    # Previous configurations and variables
    aux_time_series_set = np.copy(time_series_set); np.random.shuffle(aux_time_series_set)
    accuracy_log = np.zeros((k))
    training_set_size = int(time_series_set.shape[0]/k)
    total_time_performed = 0

    if verbose: print('\n\n<=== Starting {}-Fold Cross Validation ===>'.format(k))

    # Loops through the k iterations of the k-folds
    for i in range(k):
        training_set,testing_set = [],[]
        starting_time = time.time()

        if verbose: print('\n<--- Starting K-fold with k={} --->'.format(i))
        # When is the last k the sets are conformed so that the test
        # set remains with the same size in all iterations
        if i == (k-1): 
            testing_set = aux_time_series_set[-training_set_size:]
            training_set = np.delete(aux_time_series_set,np.s_[-training_set_size:],axis=0)
        # When k is not in the last iteration
        else:
            testing_set = aux_time_series_set[i*training_set_size:(i+1)*training_set_size]
            training_set = np.delete(aux_time_series_set,np.s_[i*training_set_size:(i+1)*training_set_size],axis=0)

        # Performs the prediction of the test set
        predictions = prediction_function(testing_set,training_set,window_size=window_size)
        # The label class is the first element of the series
        accuracy_log[i] = accuracy(testing_set[:,0],predictions)

        ending_time = time.time()-starting_time
        total_time_performed += ending_time
        if verbose: print('<--- Prediction perfomed in {}sec --->'.format(ending_time))
    if verbose: print('Accuracy log >> ',list(accuracy_log))
    print('<=== CV finished. Time : {:.4f} sec, mean accuracy : {:.2f}% ===>'.format(total_time_performed,accuracy_log.mean()*100))
    return accuracy_log.mean()

def stratified_sampling(dataset,max_possible_instances:bool=True,instances_per_class:int=20):
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

    return stratified_dataset