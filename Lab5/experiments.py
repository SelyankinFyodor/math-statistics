import numpy as np
from Lab2.num_char import numerical_characteristics as nc
from Lab5.sample_cor_coef import sample_correlation_coefficients as scc
from Lab5.presentation import *


def simple_dist_test(capacity):
    for cov in [0, 0.5, 0.9]:
        cell_text = []
        for c_cor in [
            scc.pearson,
            scc.spearman,
            scc.selective_quadrant
        ]:
            data = [c_cor(np.random.multivariate_normal((0, 0), [[1, cov], [cov, 1]], capacity).T) for _ in range(1000)]
            cell_text += [list(map(lambda x: "%.4f" % x, [
                nc.sample_mean(data),
                nc.sample_mean(list(map(lambda x: x ** 2, data))),
                nc.dispersion_exp(data)]))]
        draw_table("normal distribution n = %i, p = %.2f" % (capacity, cov), np.array(cell_text).T)


def complex_dist_test(capacity):
    def f(cap): return 0.9 * np.random.multivariate_normal((0, 0), [[1, 0.9], [0.9, 1]], cap).T + \
                        0.1 * np.random.multivariate_normal((0, 0), [[100, -0.9], [-0.9, 100]], cap).T
    cell_text = []
    for c_cor in [
        scc.pearson,
        scc.spearman,
        scc.selective_quadrant
      ]:
        data = [c_cor(f(capacity)) for _ in range(1000)]
        cell_text += [list(map(lambda x: "%.4f" % x, [
            nc.sample_mean(data),
            nc.sample_mean(list(map(lambda x: x ** 2, data))),
            nc.dispersion_exp(data)]))]
    draw_table("complex normal distribution n = %i" % capacity, np.array(cell_text).T)


def ellipse_test(capacity):
    from matplotlib.patches import Ellipse
    fig, sp = plt.subplots(1, 3, figsize=(16, 6))
    for cor, subplot in zip([0, 0.5, 0.9], sp):
        dots = np.random.multivariate_normal((0, 0), [[1, cor], [cor, 1]], capacity).T
        vx = nc.dispersion_exp(dots[0])
        vy = nc.dispersion_exp(dots[1])
        angle = np.arctan(np.sqrt(vx)*np.sqrt(vy)*cor/(vx-vy))/2
        w = 4*np.sqrt(vx*(np.cos(angle))**2 + cor*np.sqrt(vx)*np.sqrt(vy)*np.sin(2*angle) + vy*(np.sin(angle))**2)
        h = 4*np.sqrt(vx*(np.sin(angle))**2 - cor*np.sqrt(vx)*np.sqrt(vy)*np.sin(2*angle) + vy*(np.cos(angle))**2)
        ell = Ellipse(xy=(nc.sample_mean(dots[0]), nc.sample_mean(dots[1])), width=w, height=h, angle=np.rad2deg(angle))
        draw_ellipse("normal distribution p  = %.1f" % cor, ell, dots, subplot)
    plt.show()
