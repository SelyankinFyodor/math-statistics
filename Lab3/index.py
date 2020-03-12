import matplotlib.pyplot as plt
from Lab1.distribution import distribution as d
from Lab3.emissions import get_prop_emission


def show_box_plot(distribution):
    _, x = plt.subplots()
    x.boxplot([distribution(20), distribution(100)], vert=False)
    x.set_title(distribution.__name__)
    x.set_yticklabels(['20', '100'])
    x.grid()
    plt.show()


if __name__ == "__main__":
    for dist in [
        d.uniform,
        d.poisson,
        d.laplace,
        d.normal,
        d.cauchy
    ]:
        show_box_plot(dist)
        print(dist.__name__)
        print("%.6f" % get_prop_emission(dist, 20))
        print("%.6f" % get_prop_emission(dist, 100))
