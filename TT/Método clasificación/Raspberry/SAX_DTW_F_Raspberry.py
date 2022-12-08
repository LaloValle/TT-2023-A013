""" Source code for testing the performance when predicting of an embedded system as Raspberry for the SAX-DTW-Features approach
The trained model of SVM and the Representatives of the class are needed to be previously computed for this task.
"""
import numpy as np
#------------
# Parameters
#------------
number_words = 64; alphabet_size = 9
numeric_alphabet = True
window_size = 4

def recover_model_representatives():
    import joblib

    filename_model = './Results/Trained_SAX-DTW-F_SVM.sav'; filename_representatives = './Results/Class_representatives.csv'
    #======================
    # Recovering the model
    #======================
    classifier = joblib.load(filename_model)
    #================================
    # Recovering the representatives
    #================================
    representatives = np.genfromtxt(filename_representatives,delimiter=',')
    print('Representatives shape >>', representatives.shape)
    # The representatives gets transformed into the dict structure
    representatives = {int(representative[0]):representative[1:] for representative in representatives}

    return classifier,representatives

def prediction_performance_test(classifier,representatives):
    import time
    from LLibraries.SAX import to_SAX_dataset
    from LLibraries.Tools import accuracy, stratified_sampling
    from LLibraries.DTWFeatures import DTW_features_dataset
    
    #============================
    # Recovering of the datasets
    #============================
    print('\n<=== Testing process ===>\n')
    gestures_Z_dataset = []
    #----------------
    # Pebble Gesture
    #----------------
    # Z Axis
    gestures_Z_dataset = np.genfromtxt(
        './Data/GesturePebbleZ1/GesturePebbleZ1_TEST.tsv',
        dtype = np.float16,
        delimiter = '	',
        missing_values = {'NaN'},
        filling_values = {np.NaN}
    )
    #=======================
    # Processing of Dataset
    #=======================
    # The dataset gets stratified and returns as a list of arrays of potentially variable lengths
    #    It's necesary to work with a list of arrays for the time series which will be working with are of variable length
    #    thus, an structure as an array cannot work with arrays in a higher dimension with different sizes on them
    stratified_dataset = stratified_sampling(gestures_Z_dataset,max_possible_instances=True)
    print('Stratified dataset number instances >> ', len(stratified_dataset))
    # SAX discretization of the whole dataset
    #   The class label gets added as the first element of the 
    sax_dataset = to_SAX_dataset(stratified_dataset,number_words,alphabet_size,numeric_alphabet)
    print('SAX dataset length >> ', len(sax_dataset))

    #======================
    # DTW-Features vectors
    #======================
    # Array vectors with the distance between each element of the dataset with the representative of the class
    print('\n<--- Creating the training dataset with the DTW-Features instances --->')
    starting_time = time.time()
    dtw_features, dtw_features_labels, _ = DTW_features_dataset(sax_dataset,representatives=representatives,window_size=window_size)
    print('<--- Created {} DTW features vectors in {:.2f} sec --->'.format(dtw_features.shape[0],time.time()-starting_time))

    #=============
    # Testing SVC
    #=============
    print('<--- Starting predictions --->')
    predictions = classifier.predict(dtw_features)
    ending_time = time.time() - starting_time
    #results = {
    #    'Classes' : dtw_features_labels,
    #    'Predictions' : predictions
    #}
    acc = accuracy(dtw_features_labels,predictions)
    print('Accuracy >> ', acc)
    print('<--- Predictions finished, accuracy:{:.2f}% , {:.2f} sec --->'.format(acc*100,ending_time))

def main():
    classifier,representatives = recover_model_representatives()
    prediction_performance_test(classifier,representatives)

if __name__ == '__main__': main()