from Lab1.distribution import distribution as d
from Lab2.num_char import numerical_characteristics as nc

if __name__ == "__main__":
    for dist in [
        d.uniform,
        d.poisson,
        d.laplace,
        d.normal,
        d.cauchy
    ]:
        print(dist.__name__)
        for capacity in [10, 100, 1000]:
            for num_char in [
                nc.sample_mean,
                nc.median,
                nc.halfsum_extreme,
                nc.halfsum_quartile,
                nc.truncated_mean
            ]:
                print(num_char.__name__ + "  cap: " + str(capacity))
                data = []
                for _ in range(1000):
                    e = dist(capacity)
                    e.sort()
                    data.append(num_char(e))
                print("%.6f" % nc.sample_mean(data))
                print("%.6f" % nc.dispersion_exp(data))
                print('==================================')
