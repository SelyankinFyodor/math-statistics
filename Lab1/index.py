from Lab1.distribution import distribution, density
import matplotlib.pyplot as plot
import seaborn


def build_gist(exp, cap):
    x = exp['distribution'](capacity)
    x.sort()
    d = []
    for cord in x:
        d.append(exp['density'](cord))
    plot.plot(x, d, 'red')
    seaborn.distplot(x)
    plot.title("%s, capacity:%s" % (exp['distribution'].__name__, cap))
    plot.ylabel("fx")
    plot.xlabel("X")
    plot.grid()
    plot.legend(('density', 'histogram'))
    plot.show()


if __name__ == "__main__":
    for experiment in [
        {'distribution': distribution.uniform, 'density': density.uniform},
        {'distribution': distribution.poisson, 'density': density.poisson},
        {'distribution': distribution.laplace, 'density': density.laplace},
        {'distribution': distribution.normal,  'density': density.normal},
        {'distribution': distribution.cauchy,  'density': density.cauchy}
    ]:
        for capacity in [10, 50, 1000]:
            build_gist(experiment, capacity)
