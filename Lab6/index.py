from Lab6.functions import *
from matplotlib import pyplot as plt

if __name__ == "__main__":
    for m in [
        model,
        indignant_model
    ]:
        xi = [(-18 + 2*i)/10 for i in range(20)]
        yi = m(xi)
        plt.plot(xi, yi, 'ks')
        plt.plot(xi, std(xi), 'r')
        plt.plot(xi, mls_result(xi, yi, xi), 'k')
        plt.plot(xi, mlm_result(xi, yi, xi), 'y')
        plt.legend(('Выборка ', 'Модель', 'МНК', 'МНМ'))
        plt.title(m.__name__)
        plt.show()
