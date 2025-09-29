import numpy as np

def gini_coefficient(x):
    """Compute Gini coefficient of array of values"""
    diffsum = 0
    x = np.array(x)
    for i, xi in enumerate(x[:-1], 1):
        diffsum += np.sum(np.abs(xi - x[i:]))

    # print("alternative gini score: ")
    # print(alternative_gini_coefficient(x))
    return diffsum / (len(x)**2 * np.mean(x))

def lower_bound(x, size): # x=array, size,
    """Compute lower bound of Gini coefficient"""
    diffsum = 0
    x = np.array(x)
    for i, xi in enumerate(x[:-1], 1):
        diffsum += np.sum(np.abs(xi - x[i:]))
    return diffsum / (len(x)**2 * np.mean(x))

def alternative_gini_coefficient(x):
    # x.sort(reverse=True)
    x.sort()
    sum = 0
    for index, i in enumerate(x):
        sum = sum + (index + 1) * i


    return (2 * sum) / (len(x) * np.sum(x)) - (len(x) + 1) / len(x)

# e = [2, 2, 6, 156, 20, 6, 6, 12, 2, 2, 12, 6, 20, 6, 72, 2, 6, 462, 72, 20, 2, 2, 6, 6, 2, 2, 2, 20, 6, 6, 6, 2]
#
# print(gini_coefficient(e))
# print(lower_bound([2, 2, 6, 156, 20, 6, 6, 12, 2, 2, 12, 6, 20, 6, 72, 2, 6, 462, 72, 2, 2, 6, 6, 2, 2, 2, 20, 6, 6, 6, 2], len(e)-1))

# e = [1, 10]
# print(gini_coefficient(e))

# e = [1,2,3]
# print(gini_coefficient(e))
e = [5,4,4,4,4]
print(gini_coefficient(e))

e = [5,4,4,4]
print(gini_coefficient(e))