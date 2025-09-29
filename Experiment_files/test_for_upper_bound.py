import numpy as np

def lower_bound(x, n):  # x=array, size,
    x.sort()
    m = len(x)
    D = n - m
    C = np.sum([(i + 1) * n for i, n in enumerate(x)])
    sum_x = sum(x)

    return (2 * (D * (1 + D) * np.min(x) / 2 + D * sum_x + C)) / (n * (sum_x + D * np.max(x))) - ((n + 1) / n)

def lower_bound2(x, n):  # x=array, size,
    x.sort()
    m = len(x)
    D = n - m
    C = np.sum([(i + 1) * n for i, n in enumerate(x)])
    sum_x = sum(x)

    last_item = np.sum([(2*(i+1) - 1) * n for i, n in enumerate(x)])

    return ( D*D*np.min(x) + 2 * D * sum_x + last_item ) / (n * (sum_x + D * np.max(x))) - 1


def lower_bound3(x, n):  # x=array, size,

    x_ = [i for i in x]
    for _ in range(0, n-len(x)):
        x_.append( np.median(x_) )

    top = 0
    for i in x_:
        for j in x_:
            top = top + np.absolute(i-j)

    # m = len(x)
    # D = n - m
    # C = np.sum([(i + 1) * n for i, n in enumerate(x)])
    # sum_x = sum(x)
    #
    # last_item = np.sum([(2*(i+1) - 1) * n for i, n in enumerate(x)])

    return top / (2 * n * (np.sum(x) + (n - len(x)) * np.max(x) ))

    # return top / (2 * n * (np.sum(x_)))


def lower_bound4(x, n):  # x=array, size,

    x_ = [i for i in x]
    x_.append( np.median(x_) )

    top = 0
    for i in x_:
        for j in x_:
            top = top + np.absolute(i-j)

    return top / (2 * n * (np.sum(x) + np.max(x) ))


def gini_coefficient(x):
    """Compute Gini coefficient of array of values"""
    diffsum = 0
    x = np.array(x)
    for i, xi in enumerate(x[:-1], 1):
        diffsum += np.sum(np.abs(xi - x[i:]))

    # print("alternative gini score: ")
    # print(alternative_gini_coefficient(x))
    return diffsum / (len(x)**2 * np.mean(x))


def alternative_gini_coefficient(x):
    # x.sort(reverse=True)
    x.sort()
    sum = 0
    for index, i in enumerate(x):
        sum = sum + (index + 1) * i


    return (2 * sum) / (len(x) * np.sum(x)) - (len(x) + 1) / len(x)


def alternative_gini_coefficient2(x):
    # x.sort(reverse=True)
    x.sort()
    sum = 0
    for index, i in enumerate(x):
        sum = sum + (2*(index + 1)-1) * i


    return sum / (len(x) * np.sum(x)) - 1

def test1(x, n):
    x_ = [i for i in x]
    median = np.median(x_)

    for _ in range(0, n - len(x)):
        x_.append( median )

    top = 0
    for i in x_:
        for j in x_:
            top = top + np.absolute(i-j)

    return top

def test2(x, n):
    x_ = [i for i in x]
    for _ in range(0, n - len(x)):
        x_.append( np.median(x_) )

    top = 0
    for i in x_:
        for j in x_:
            top = top + np.absolute(i - j)

    return top
# e = [2, 2, 6, 156, 20, 6, 6, 12, 2, 2, 12, 6, 20, 6, 72, 2, 6, 462, 72, 20, 2, 2, 6, 6, 2, 2, 2, 20, 6, 6, 6, 2]
#
# print(gini_coefficient(e))
# print(lower_bound([2, 2, 6, 156, 20, 6, 6, 12, 2, 2, 12, 6, 20, 6, 72, 2, 6, 462, 72, 2, 2, 6, 6, 2, 2, 2, 20, 6, 6, 6, 2], len(e)-1))

# e = [1, 10]
# print(gini_coefficient(e))

# e = [1,2,3]
# print(gini_coefficient(e))
e = [4,4,4,4,4,4,4,3,1]
e_ = [4,1,3]
print("Gini: " + str(gini_coefficient(e)))
print("Alternative Gini: " + str(alternative_gini_coefficient(e)))
print("Alternative Gini2: " + str(alternative_gini_coefficient2(e)))

print("Lower bound: " + str(lower_bound(e_, 9)))
print("Lower bound2: " + str(lower_bound2(e_, 9)))
print("Lower bound3: " + str(lower_bound3(e_, 9)))
print("Lower bound4: " + str(lower_bound4(e_, 9)))

from scipy.misc import derivative


def f(x):
    a = [1,2,4,5]
    a.append(x)
    a.sort()
    return alternative_gini_coefficient2(a)

# print(derivative(f, 3, dx=1e-6))

def f1(x):
    a = [1,4,5,6]
    a.append(x)
    a.sort()
    return alternative_gini_coefficient2(a)

def f2(x):
    a = [1,2,5,6]
    a.append(x)
    a.sort()
    return alternative_gini_coefficient2(a)

print(f1(3)-f(3))

print(f2(3)-f(3))


# print("Lower bound: " + str(lower_bound(e_, 8)))
# print("Lower bound2: " + str(lower_bound2(e_, 8)))
# print("Lower bound3: " + str(lower_bound3(e_, 8)))

# e = [1,4,6,10]
#
# print(test1(e, 8))
#
# print(test2(e, 8))
# print(test2(e_, 5))
#
# e__ = [15,15,15,14, 15.01]
# print(test1(e__))

e = [12,2,2,2,2]
# e = [12,2,2,2,2]
e_ = [2,2,2]
# e__ = [0,10,50,45]
print("Gini: " + str(gini_coefficient(e)))
print("Gini: " + str(gini_coefficient(e_)))
# print("Gini: " + str(gini_coefficient(e__)))
# print("Alternative Gini: " + str(alternative_gini_coefficient(e)))
# print("Lower bound: " + str(lower_bound(e_, 3)))
# print("Lower bound2: " + str(lower_bound2(e_, 3)))
# print("Lower bound3: " + str(lower_bound3(e_, 3)))
