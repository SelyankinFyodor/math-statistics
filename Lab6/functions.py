from Lab1.distribution import distribution as d
from Lab2.num_char import numerical_characteristics as nc
import numpy as np


def model(x):
    return [2 + 2 * dot + ei for dot, ei in zip(x, d.normal(20))]


def indignant_model(x):
    y = [2 + 2 * dot + ei for dot, ei in zip(x, d.normal(20))]
    y[0] += 10
    y[19] -= 10
    return y


def std(x):
    return [2 + 2 * e for e in x]


def mls_result(x, y, interval):
    b_1 = (nc.sample_mean(np.array(x) * np.array(y)) - nc.sample_mean(x) * nc.sample_mean(y)) / (
            nc.sample_mean(list(map(lambda e: e ** 2, x))) - nc.sample_mean(x) ** 2)
    b_0 = nc.sample_mean(y) - nc.sample_mean(x) * b_1
    print("mml coefficients:: a:%.2f,  b:%.2f" % (b_0, b_1))
    return [b_0 + b_1 * e for e in interval]


def mlm_result(x, y, interval):
    n = len(x)
    med_x = nc.median(sorted(x))
    med_y = nc.median(sorted(y))
    rq = sum(np.array(list(map(lambda e: np.sign(e - med_x), x))) *
             np.array(list(map(lambda e: np.sign(e - med_y), y)))) / n
    l_index = n // 4 + 1 if n % 4 != 0 else n // 4
    b_1r = rq * (y[n - l_index + 1] - y[l_index]) / (x[n - l_index + 1] - x[l_index])
    b_0r = med_y - b_1r * med_x
    print("mml coefficients:: a:%.2f,  b:%.2f" % (b_0r, b_1r))
    return [b_0r + b_1r * e for e in interval]
