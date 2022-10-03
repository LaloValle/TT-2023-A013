import pandas as ps
import numpy as np
import matplotlib.pyplot as plt
from tslearn.barycenters import dtw_barycenter_averaging
# Local Libraries
from LLibraries.SAX import *
from LLibraries.DTWWindowOptimizer import *
from LLibraries.Tools import group_by_class, stratified_sampling

def tests():
    #============================
    # Recovering of the datasets
    #============================
    gestures_Z_dataset = []
    number_words = 32; alphabet_size = 7
    numeric_alphabet = True
    #----------------
    # Pebble Gesture
    #----------------
    # Z Axis
    gestures_Z_dataset = np.genfromtxt(
        './Data/GesturePebbleZ1/GesturePebbleZ1_TRAIN.tsv',
        dtype = np.float16,
        delimiter = '	',
        missing_values = {'NaN'},
        filling_values = {np.NaN}
    )
    # Class labels
    unique_labels = np.unique(gestures_Z_dataset[:,0])
    print('Number of classes >> ', unique_labels.size)
    print('Max lenght time series >> ', gestures_Z_dataset.shape[1])

    #=======================
    # Processing of Dataset
    #=======================
    # The dataset gets stratified and returns as a list of arrays of potentially variable lengths
    #    It's necesary to work with a list of arrays for the time series which will be working with are of variable length
    #    thus, an structure as an array cannot work with arrays in a higher dimension with different sizes on them
    stratified_dataset = stratified_sampling(gestures_Z_dataset,max_possible_instances=False,instances_per_class=5)
    print('Stratified dataset number instances >> ', len(stratified_dataset))
    # Grouping by class the series
    dataset_by_classes = group_by_class(stratified_dataset)
    print('Classes >> ', list(dataset_by_classes.keys()))

    #======================
    # Barycenter Averaging
    #======================
    dtwba = dtw_barycenter_averaging(dataset_by_classes[1], max_iter=50, tol=1e-3)

    #==========
    # Plotting
    #==========
    fig,axs = plt.subplots(1)
    #------------
    # Raw series
    #------------
    # 5 Series
    for index in range(5):
        axs.plot([x for x,_ in enumerate(dataset_by_classes[1][index][1:])],dataset_by_classes[1][index][1:],linewidth=0.5,color='k')
        axs.scatter([x for x,_ in enumerate(dataset_by_classes[1][index][1:])],dataset_by_classes[1][index][1:])
    axs.plot([x for x,_ in enumerate(dtwba)],dtwba,linewidth=1.2,color='r')
    # Series 2
    # axs[1].plot([x for x,_ in enumerate(dtwba)],list(dtwba))
    # axs[1].scatter([x for x,_ in enumerate(dataset_by_classes[1][1][1:])],list(dataset_by_classes[1][1][1:]))

    plt.show()




def main():
    tests()

if __name__ == '__main__': main()