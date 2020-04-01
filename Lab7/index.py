import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from Lab1.distribution import distribution as d, density as den
from Lab2.num_char import numerical_characteristics as nc

if __name__ == "__main__":
    n = 100
    k = 7
    delta = 0.5
    x_i = sorted(d.normal(n))
    m0 = nc.sample_mean(x_i)
    d = nc.dispersion_exp(x_i)
    print("%.2f %.2f" % (m0, d))
    d_i = [
        [-np.inf, m0-delta*2.5],
        [m0-delta*2.5, m0-delta*1.5],
        [m0-delta*1.5, m0-delta*0.5],
        [m0-delta*0.5, m0+delta*0.5],
        [m0+delta*0.5, m0+delta*1.5],
        [m0+delta*1.5, m0+delta*2.5],
        [m0+delta*2.5, np.inf]
    ]
    n_i = [0]*k
    for x in x_i:
        for i in range(k):
            if d_i[i][0] < x <= d_i[i][1]:
                n_i[i] += 1
    p_i = [integrate.quad(den.normal, i[0], i[1])[0] for i in d_i]
    npi = n*np.array(p_i)
    ni_npi = np.array(n_i) - npi
    xi_2_B = ((np.array(n_i) - n * np.array(p_i)) ** 2) / (n * np.array(p_i))
    cell_text = list(np.array([
        list(map(lambda i: "%.2f, %.2f" % (i[0], i[1]), d_i)),
        list(n_i),
        list(map(lambda i: "%.4f" % i, p_i)),
        list(map(lambda i: "%.2f" % i, npi)),
        list(map(lambda i: "%.2f" % i, ni_npi)),
        list(map(lambda i: "%.2f" % i, xi_2_B))
    ]).T) + [["-", sum(n_i), "%.4f" % sum(p_i), "%.2f" % sum(npi), "%.2f" % sum(ni_npi), "%.2f" % sum(xi_2_B)]]

    fig, axs = plt.subplots(1, 1, figsize=(16, 6))
    axs.axis('off')
    axs.table(colLabels=["borders", "ni", "pi", "npi", "ni-npi", "(ni-npi)^2 / npi"],
              rowLabels=[str(i+1) for i in range(k)] + ["sum"],
              cellText=cell_text, loc="center")
    fig.show()
