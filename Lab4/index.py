from Lab1.distribution import distribution as d
from Lab1.distribution import density as den

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def draw_cdf(e, cap, subplot):
    subplot.set_title(e['dist'].__name__ + ' capacity=' + str(cap))
    samples = sorted(e['dist'](cap))
    res = stats.cumfreq(samples, numbins=cap, defaultreallimits=e['section'])
    x = min(e['section']) + np.linspace(0, res.binsize * res.cumcount.size, res.cumcount.size)
    subplot.bar(x, res.cumcount / cap, width=res.binsize)
    subplot.set_ylim([0, 1.2])
    subplot.set_xlim([min(e['section']) - 1, max(e['section']) + 1])


def draw_kde(e, cap, subplot):
    def kde(samples, param):
        k = stats.gaussian_kde(samples, bw_method="silverman")
        k.set_bandwidth(k.factor*param)
        return k
    subplot.set_title(e['dist'].__name__ + ' capacity=' + str(cap))
    sample = sorted(e['dist'](cap))
    x = np.linspace(min(e['section']), max(e['section']), 10000, endpoint=True)
    for p in [0.5, 1.0, 2.0]:
        subplot.plot(sample, kde(samples=sample, param=p)(sample), label="h = %.1f * hn" % p)
    subplot.plot(x, list(map(e['dens'], x)), label="func")
    subplot.grid()
    subplot.legend()
    subplot.set_ylim([0, 1.2])
    subplot.set_xlim([min(e['section']) - 1, max(e['section']) + 1])


if __name__ == "__main__":
    for exp in [
        {'dist': d.uniform, 'section': [-4, 4], 'dens': den.uniform},
        {'dist': d.poisson, 'section': [6, 14], 'dens': den.poisson},
        {'dist': d.laplace, 'section': [-4, 4], 'dens': den.laplace},
        {'dist': d.normal, 'section': [-4, 4], 'dens': den.normal},
        {'dist': d.cauchy, 'section': [-4, 4], 'dens': den.cauchy}
    ]:
        for draw in [draw_cdf, draw_kde]:
            fig, axs = plt.subplots(1, 3, figsize=(16, 6))
            for capacity, plot in zip([20, 60, 100], axs):
                draw(exp, capacity, plot)
            plt.show()
