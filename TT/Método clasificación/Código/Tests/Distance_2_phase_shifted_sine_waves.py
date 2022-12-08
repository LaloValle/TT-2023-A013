import random
# Numpy import
import numpy as np
# Matplotlib import
import matplotlib.pyplot as plt
# DTW algorithm and visualization
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis


# Uniform distribution of point between 0 and 20 with steps of 0.5
x = np.arange(0, 20, 0.5)
# Sine waves
sine_1 = np.sin(x)
sine_2 = np.sin(x - 1) # Sifted phase sine

series_1 = [ 0, 0.5, 0.8, 1.4, 0.9, 1.3 ]
series_2 = [ 0.3, 0.5, 1.2, 1.6, 1]

# DTW algorithm
path = dtw.warping_path(sine_1, sine_2)
# Visualisation of the optimal correspondence between sines
figure,ax = dtwvis.plot_warping(sine_1, sine_2, path)
distance = dtw.distance(sine_1, sine_2)

# DTW algorithm
path_2 = dtw.warping_path(series_1, series_2)
# Visualisation of the optimal correspondence between sines
figure_2,ax_2 = dtwvis.plot_warping(series_1, series_2, path_2)
distance_2 = dtw.distance(series_1, series_2)

# Results
print('Path >>', path)
print('Distance >>', distance)
print('Path 2 >>', path_2)
print('Distance 2 >>', distance_2)
plt.show()