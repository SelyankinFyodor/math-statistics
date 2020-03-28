import numpy as np
from Lab2.num_char import numerical_characteristics as nc
from Lab5.sample_cor_coef import sample_correlation_coefficients as scc
from Lab5.presentation import *


def simple_dist_test(capacity):
    for cov in [0, 0.5, 0.9]:
        data = []
        for _ in range(1000):
            sample = np.random.multivariate_normal((0, 0), [[1, cov], [cov, 1]], capacity).T
            data += [[c_cor(sample) for c_cor in [scc.pearson, scc.spearman, scc.selective_quadrant]]]
        data = np.array(data).T
        cell_text = [list(map(lambda x: "%.4f" % x, [
            nc.sample_mean(data[i]),
            nc.sample_mean(list(map(lambda x: x ** 2, data[i]))),
            nc.dispersion_exp(data[i])])) for i in range(3)]
        draw_table("normal distribution n = %i, p = %.2f" % (capacity, cov), np.array(cell_text).T)


def complex_dist_test(capacity):
    def f(cap): return 0.9 * np.random.multivariate_normal((0, 0), [[1, 0.9], [0.9, 1]], cap).T + \
                        0.1 * np.random.multivariate_normal((0, 0), [[100, -0.9], [-0.9, 100]], cap).T
    data = np.array([[c_cor(f(capacity)) for c_cor in [scc.pearson, scc.spearman, scc.selective_quadrant]]
                     for _ in range(1000)]).T
    cell_text = [list(map(lambda x: "%.4f" % x, [
        nc.sample_mean(data[i]),
        nc.sample_mean(list(map(lambda x: x ** 2, data[i]))),
        nc.dispersion_exp(data[i])])) for i in range(3)]
    draw_table("complex normal distribution n = %i" % capacity, np.array(cell_text).T)


def ellipse_test(capacity):
    from matplotlib.patches import Ellipse
    _, sp = plt.subplots(1, 3, figsize=(16, 6))
    for cor, subplot in zip([0, 0.5, 0.9], sp):
        dots = np.random.multivariate_normal((0, 0), [[1, cor], [cor, 1]], capacity).T
        vx = nc.dispersion_exp(dots[0])
        vy = nc.dispersion_exp(dots[1])
        angle = np.arctan(np.sqrt(vx)*np.sqrt(vy)*cor/(vx-vy))/2
        w = 5*np.sqrt(vx*(np.cos(angle))**2 + cor*np.sqrt(vx)*np.sqrt(vy)*np.sin(2*angle) + vy*(np.sin(angle))**2)
        h = 5*np.sqrt(vx*(np.sin(angle))**2 - cor*np.sqrt(vx)*np.sqrt(vy)*np.sin(2*angle) + vy*(np.cos(angle))**2)
        ell = Ellipse(xy=(nc.sample_mean(dots[0]), nc.sample_mean(dots[1])), width=w, height=h, angle=np.rad2deg(angle))
        draw_ellipse("normal distribution %s = %.1f" % (r'$\rho$', cor), ell, dots, subplot)
    plt.show()
