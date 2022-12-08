import numpy as np

def choose_initial_average_series(dataset):
    """Choose an initial average series in a determinstic fashion.
    For each series records the average height of the whole series and then chooses the median series of the dataset
    """
    average_height = np.array([np.average(instance) for instance in dataset])
    median_index_series = average_height.argsort()[int(len(dataset)/2)]
    return dataset[median_index_series]

def representatives_by_class(dataset:list,with_initial_barycenter:bool=False):
    from LLibraries.Tools import group_by_class
    from tslearn.barycenters import dtw_barycenter_averaging

    aux_dataset = dict(); representatives = dict()
    
    # If the dataset given is a dictionary then it's already divided by class
    if type(dataset) == dict: aux_dataset = dict(dataset)
    # Otherwise first the dataset must be organized by class
    else: aux_dataset = group_by_class(dataset)

    for label in aux_dataset.keys():
        if with_initial_barycenter:
            representatives[label] = dtw_barycenter_averaging(aux_dataset[label], max_iter=50, tol=1e-3, init_barycenter=choose_initial_average_series(aux_dataset[label])).reshape((-1))
        else:
            representatives[label] = dtw_barycenter_averaging(aux_dataset[label], max_iter=50, tol=1e-3).reshape((-1))
    
    return representatives

def DTW_features_dataset(dataset,representatives:dict=dict(),with_initial_barycenter:bool=False,window_size:int=0):
    from LLibraries.DTW import DTW
    
    # Verifies the dictionary with the representatives of each class has been already calculated
    if not representatives: 
        print('<!!! Representatives computed !!!>')
        representatives = representatives_by_class(dataset,with_initial_barycenter)
    
    dtw_features = np.empty((len(dataset),len(representatives)))
    dtw_features_labels = np.array([instance[0] for instance in dataset])

    labels = list(representatives.keys()); labels.sort()
    for feature_column in range(len(labels)):
        dtw_features[:,feature_column] = [DTW(instance[1:],representatives[labels[feature_column]],window_size=window_size) for instance in dataset]

    return dtw_features,dtw_features_labels,representatives

def tabular_DTW_features_with_label(dtw_features,labels):
    import pandas as ps
    
    uniques = list(np.unique(labels)); uniques.sort()

    data = {
        'Labels' : labels
    }
    for feature in range(dtw_features.shape[1]):
        data['Class {}'.format(uniques[feature])] = dtw_features[:,feature]

    return ps.DataFrame(data)

def SAX_DTWF_SVC(classification_set:list,training_set:list,representatives:dict=dict(),window_size:int=0,**kargs):
    import time
    from sklearn import svm
    
    #======================
    # DTW-Features vectors
    #======================
    # Array vectors with the distance between each element of the dataset with the representative of the class
    print('\n<--- Creating the training dataset with the DTW-Features instances --->')
    dtw_training_set, dtw_training_set_labels, representatives = DTW_features_dataset(training_set,representatives,window_size=window_size)
    dtw_classification_set, _, _ = DTW_features_dataset(classification_set,representatives,window_size=window_size)

    #=====
    # SVC 
    #=====
    # Creates the Support Vector Machine Classifier
    classifier = svm.SVC(C=1,gamma='scale',degree=3,kernel='poly')
    # Trains the model
    print('<--- Training the model SVC --->')
    starting_time = time.time()
    classifier.fit(dtw_training_set,dtw_training_set_labels)
    ending_time = time.time() - starting_time
    print('<--- Model training finished: {} sec --->\n'.format(ending_time))

    # Tests the model
    return classifier.predict(dtw_classification_set)