import numpy as np


def get_prop_emission(dist, size):
    data = []
    num_of_experiments = 1000
    for _ in range(num_of_experiments):
        sample = dist(size)
        x1 = np.quantile(sample, 0.25) - 3 / 2 * ((np.quantile(sample, 0.75)) - (np.quantile(sample, 0.25)))
        x2 = np.quantile(sample, 0.75) + 3 / 2 * ((np.quantile(sample, 0.75)) - (np.quantile(sample, 0.25)))
        data.append(len(list(filter(lambda x: x < x1 or x > x2, sample)))/size)
    return sum(data)/num_of_experiments
