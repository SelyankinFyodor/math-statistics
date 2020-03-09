import numpy as np
import math


class distribution:
    @staticmethod
    def normal(size):
        return np.random.standard_normal(size=size)

    @staticmethod
    def cauchy(size):
        return np.random.standard_cauchy(size=size)

    @staticmethod
    def laplace(size):
        return np.random.laplace(scale=1/math.sqrt(2), size=size)

    @staticmethod
    def poisson(size):
        return np.random.poisson(lam=10, size=size)

    @staticmethod
    def uniform(size):
        return np.random.uniform(low=-math.sqrt(3), high=math.sqrt(3), size=size)


class density:
    @staticmethod
    def normal(x):
        return math.exp(-(x * x) / 2) / math.sqrt(2 * math.pi)

    @staticmethod
    def cauchy(x):
        return (1 / math.pi) * (1 / (x * x + 1))

    @staticmethod
    def laplace(x):
        return (1 / math.sqrt(2)) * math.exp(-math.sqrt(2) * math.fabs(x))

    @staticmethod
    def poisson(k):
        return (math.pow(10, k) / math.factorial(k)) * math.exp(-10)

    @staticmethod
    def uniform(x):
        return 1 / (2 * math.sqrt(3)) if math.fabs(x) <= math.sqrt(3) else 0
