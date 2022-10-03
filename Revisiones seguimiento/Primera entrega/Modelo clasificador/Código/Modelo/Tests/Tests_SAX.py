import numpy as np
import matplotlib.pyplot as plt
from LLibraries.DTW import *
from LLibraries.SAX import *
from Libraries.Tools import standardize

def main():
    prueba_2_PAA()



def prueba_PAA():
    number_words = 5; alphabet_size = 3

    series_1 = np.array([ 0, 0.5, 0.8, 1.4, 0.9, 1.3 ])
    series_1_std = standardize((series_1))
    print('Time series >>',series_1)
    print('Normalized time series >>',series_1_std)

    aproximation = PAA(series_1_std,number_words)
    print('PAA >>',aproximation)

    sax_string = SAX(series_1,number_words,alphabet_size)
    print('SAX >> ',sax_string)

    plt.plot([x for x,_ in enumerate(series_1_std)],series_1_std)
    plt.scatter([x for x,_ in enumerate(series_1_std)],series_1_std)
    plt.plot([x for x,_ in enumerate(aproximation)],aproximation)
    plt.scatter([x for x,_ in enumerate(aproximation)],aproximation)
    for bound in equiprobable_breakpoints[str(alphabet_size)]:
        plt.plot([x for x,_ in enumerate(series_1_std)],[bound]*len(series_1_std),color='k')
    plt.show()

def prueba_2_PAA():
    #
    # https://jmotif.github.io/sax-vsm_site/morea/algorithm/SAX.html
    #
    number_words = 9; alphabet_size = 4
    numeric_alphabet = True

    # Raw series
    series_1 = np.array([2.02, 2.33, 2.99, 6.85, 9.20, 8.80, 7.50, 6.00, 5.85, 3.85, 4.85, 3.85, 2.22, 1.45, 1.34])
    series_2 = np.array([0.50, 1.29, 2.58, 3.83, 3.25, 4.25, 3.83, 4.22, 5.63, 6.44, 6.25, 7.52, 8.75, 8.83, 3.25, 2.90, 1.15, 0.75, 0.72])
    """ series_1 = np.array([0,4,2,1,7,6,3,5])
    series_2 = np.array([2,5,4,5,3,4,2,3]) """
    # Normalized series
    std_series_1 = standardize(series_1)
    std_series_2 = standardize(series_2)
    # PAA discretization
    discrete_series_1 = PAA(std_series_1,number_words)
    discrete_series_2 = PAA(std_series_2,number_words)
    # SAX strings
    sax_series_1 = SAX(series_1,number_words,alphabet_size,numeric_alphabet)
    sax_series_2 = SAX(series_2,number_words,alphabet_size,numeric_alphabet)

    print(type(discrete_series_1))
    print('SAX string 1 >> ', sax_series_1)
    print('SAX string 2 >> ', sax_series_2)

    print('SAX Distance >> ', SAX_distance(sax_series_1,sax_series_2,alphabet_size=alphabet_size))

    dtw_distance,warping_path = DTW_complete([int(digit) for digit in sax_series_1],[int(digit) for digit in sax_series_2])
    print('DTW distance >> ', dtw_distance)
    print('Warping path >> ', warping_path)

    sax_dtw_distance = SAX_DTW_distance(sax_series_1,sax_series_2,alphabet_size,warping_path)
    print('SAX-DTW distance >> ', sax_dtw_distance)

    #==========
    # Plotting
    #==========
    fig,axs = plt.subplots(2,2)
    #------------
    # Raw series
    #------------
    # Series 1
    axs[0][0].plot([x for x,_ in enumerate(series_1)],series_1)
    axs[0][0].scatter([x for x,_ in enumerate(series_1)],series_1)
    # Series 2
    axs[0][0].plot([x for x,_ in enumerate(series_2)],series_2)
    axs[0][0].scatter([x for x,_ in enumerate(series_2)],series_2)
    axs[0][0].set_title('Raw time series')
    axs[0][0].set_ylabel('a)')
    #-------------------
    # Normalized series
    #-------------------
    # Series 1
    axs[0][1].plot([x for x,_ in enumerate(std_series_1)],std_series_1)
    axs[0][1].scatter([x for x,_ in enumerate(std_series_1)],std_series_1)
    # Series 2
    axs[0][1].plot([x for x,_ in enumerate(std_series_2)],std_series_2)
    axs[0][1].scatter([x for x,_ in enumerate(std_series_2)],std_series_2)
    axs[0][1].set_title('Standardize time series')
    axs[0][1].set_ylabel('b)')
    #---------------------
    # Discrete PAA series
    #---------------------
    # Series 1
    axs[1][0].plot([x for x,_ in enumerate(discrete_series_1)],discrete_series_1)
    axs[1][0].scatter([x for x,_ in enumerate(discrete_series_1)],discrete_series_1)
    # Series 2
    axs[1][0].plot([x for x,_ in enumerate(discrete_series_2)],discrete_series_2)
    axs[1][0].scatter([x for x,_ in enumerate(discrete_series_2)],discrete_series_2)
    axs[1][0].set_title('PAA time series with number of words {}'.format(number_words))
    axs[1][0].set_ylabel('c)')
    #-------------------
    # SAX string series
    #-------------------
    # Series 1
    axs[1][1].plot([x for x,_ in enumerate(discrete_series_1)],discrete_series_1,color='steelblue',alpha=0.15)
    axs[1][1].scatter([x for x,_ in enumerate(discrete_series_1)],discrete_series_1,color='steelblue',alpha=0.15)
    # Series 2
    axs[1][1].plot([x for x,_ in enumerate(discrete_series_2)],discrete_series_2,color='darkorange',alpha=0.15)
    axs[1][1].scatter([x for x,_ in enumerate(discrete_series_2)],discrete_series_2,color='darkorange',alpha=0.15)
    # Series with breakpoints
    extended_breakpoints = [min([np.min(discrete_series_1),np.min(discrete_series_2)])] + equiprobable_breakpoints[str(alphabet_size)] + [max([np.max(discrete_series_1),np.max(discrete_series_2)])]
    mid_breakpoinst = []
    for i in range(len(extended_breakpoints)-1):
        mid_breakpoinst.append((extended_breakpoints[i]+extended_breakpoints[i+1])/2)
    # Series 1 breakpoints
    axs[1][1].plot([x for x,_ in enumerate(discrete_series_1)],[mid_breakpoinst[int(value)] for value in sax_series_1],color='steelblue')
    axs[1][1].scatter([x for x,_ in enumerate(discrete_series_1)],[mid_breakpoinst[int(value)] for value in sax_series_1],color='steelblue')
    # Series 2 breakpoints
    axs[1][1].plot([x for x,_ in enumerate(discrete_series_2)],[mid_breakpoinst[int(value)] for value in sax_series_2],color='darkorange')
    axs[1][1].scatter([x for x,_ in enumerate(discrete_series_2)],[mid_breakpoinst[int(value)] for value in sax_series_2],color='darkorange')
    # Breakpoints
    for bound in equiprobable_breakpoints[str(alphabet_size)]:
        plt.plot([x for x,_ in enumerate(discrete_series_1)],[bound]*len(discrete_series_1),color='k',linewidth=0.5,alpha=0.5)
    axs[1][1].set_title('SAX time series with number of words {} and alphabet size {}'.format(number_words,alphabet_size))
    axs[1][1].set_ylabel('d)')

    plt.show()


if __name__ == '__main__': main()