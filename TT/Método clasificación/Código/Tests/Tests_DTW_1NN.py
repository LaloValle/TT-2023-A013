import time
import numpy as np
import matplotlib.pyplot as plt
from Libraries.DTW import *
from Libraries.Tools import accuracy

def main():
    test_DTW_1KNN()



def test_DTW():
    series_1 = []; series_2 = []

    """ for x in np.arange(0,5.25,0.25)*5:
        series_1.append((x,sin(x)))
        series_2.append((x+0.5,sin(x+0.5))) """
    series_1 = [ 0, 0.5, 0.8, 1.4, 0.9, 1.3 ]
    series_2 = [ 0.3, 0.5, 1.2, 1.6, 1]
    
    # Uniform distribution of point between 0 and 20 with steps of 0.5
    x = np.arange(0, 20, 0.5)
    # Sine waves
    sine_1 = np.sin(x)
    sine_2 = np.sin(x - 1) # Sifted phase sine

    # cost_warping_path = DTW(series_1=[y for _,y in series_1],series_2=[y for _,y in series_2])
    cost_warping_path,path = DTW(series_1=series_1,series_2=series_2,window_size=3,compute_path=True)
    print('Cost optimal warping path >>',cost_warping_path)
    print('Path >>',path)
    cost_warping_path,path = DTW(series_1=sine_1,series_2=sine_2,window_size=3,compute_path=True)
    print('Cost optimal warping path >>',cost_warping_path)
    print('Path >>',path)

    LB_sum = LB_Keogh(series_1,series_2,3)
    LB_sum_2 = LB_Keogh(sine_1,sine_2,3)
    print('LB sum >>',LB_sum)
    print('LB sum >>',LB_sum_2)

    """plt.plot([x for x,_ in series_1],[y for _,y in series_1])
    plt.plot([x-series_2[0] for x,_ in series_2],[y for _,y in series_2]) """
    plt.plot([x for x,_ in enumerate(series_1)],series_1)
    plt.plot([x-series_2[0] for x,_ in enumerate(series_2)],series_2)
    plt.show()

def test_DTW_1KNN():
    train = np.genfromtxt('Data/train.csv', delimiter='\t')
    test = np.genfromtxt('Data/test.csv', delimiter='\t')
    test_2 = np.array([test[15],test[70],test[115],test[187],test[234],test[270],test[299]])
    
    time_start = time.time()
    predictions = DTW_1NN(test,train,4)
    print('Time >> ',time.time()-time_start)

    predictions = np.array(predictions)
    # print(report)

    # First proposal of finding the number of negatives
    #
    # Taken time: 5.74...e-5 sec
    #
    time_start = time.time()
    dif = test[:,-1]-predictions
    dif[dif != 0] = 1
    acc = (len(test)-dif.sum())/len(test)
    print(' Time >> ', time.time()-time_start, ' Accuracy >>',acc)

    # First proposal of finding the number of positives
    #
    # Taken time: 2.74...e-5 sec
    #
    time_start = time.time()
    dif = np.where(test[:,-1] == predictions, 1, 0)
    acc = dif.sum()/len(test)
    print('Time >> ', time.time()-time_start,' Accuracy >>', acc)

    # Second proposal of finding the number of positives
    #
    # Taken time: 1.40...e-5 sec
    # *********** Best option **************
    #
    time_start = time.time()
    acc = accuracy(test[:,-1], predictions)
    print('Time >> ', time.time()-time_start,' Accuracy >>', acc)


if __name__ == '__main__': main()