import scipy.stats as st
import numpy as np
from Lab1.distribution import distribution as d
from Lab2.num_char import numerical_characteristics as nc


if __name__ == "__main__":
    alpha = 0.05
    for n in [20, 100]:
        print("=========%i==========" % n)
        x = d.normal(n)
        m = nc.sample_mean(x)
        s = np.sqrt(nc.dispersion_exp(x))
        print("m: %.2f, %.2f" % (
            m - s*(st.t.ppf(1-alpha/2, n-1))/np.sqrt(n-1),
            m + s*(st.t.ppf(1-alpha/2, n-1))/np.sqrt(n-1)))
        print("sigma: %.2f, %.2f" % (
            s*np.sqrt(n)/np.sqrt(st.chi2.ppf(1-alpha/2, n-1)),
            s*np.sqrt(n)/np.sqrt(st.chi2.ppf(alpha/2, n-1))))
        print("m asymptotic :%.2f, %.2f" % (
            m - st.norm.ppf(1-alpha / 2)/np.sqrt(n),
            m + st.norm.ppf(1 - alpha / 2)/np.sqrt(n)))
        e = (sum(list(map(lambda el: (el-m)**4, x)))/n)/s**4 - 3
        print("sigma asymptotic: %.2f, %.2f" % (
                s/np.sqrt(1+st.norm.ppf(1-alpha / 2)*np.sqrt((e+2)/n)),
                s/np.sqrt(1-st.norm.ppf(1-alpha / 2)*np.sqrt((e+2)/n))
            )
        )



