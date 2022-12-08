from LLibraries.DTW import optimal_warping_path,DTW_complete

print(optimal_warping_path([1, 2, 3], [1., 2., 2., 3.]))
print(DTW_complete([1, 2, 3], [1., 2., 2., 3.])[::-1])