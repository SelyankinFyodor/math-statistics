from Lab2.num_char import numerical_characteristics as nc
import numpy as np


class sample_correlation_coefficients:
    @staticmethod
    def pearson(samples):
        ex = nc.sample_mean(samples[0])
        ey = nc.sample_mean(samples[1])
        sdx = np.sqrt(nc.dispersion_exp(samples[0]))
        sdy = np.sqrt(nc.dispersion_exp(samples[1]))
        return (nc.sample_mean(np.array(samples[0])*np.array(samples[1])) - ex * ey) / (sdx * sdy)

    @staticmethod
    def selective_quadrant(samples):
        n1, n2, n3, n4 = 0, 0, 0, 0
        mx, my = nc.sample_mean(samples[0]), nc.sample_mean(samples[1])
        for i in range(len(samples[0])):
            if samples[0][i] > mx and samples[1][i] >= my:
                n1 += 1
            elif samples[0][i] <= mx and samples[1][i] > my:
                n2 += 1
            elif samples[0][i] < mx and samples[1][i] <= my:
                n3 += 1
            elif samples[0][i] >= mx and samples[1][i] < my:
                n4 += 1
        return ((n1 + n3) - (n2 + n4)) / len(samples[0])

    @staticmethod
    def spearman(samples):
        def ranging(s):
            r = [-1]*len(s)
            cnt = 0
            for j in range(len(s)):
                m_i = 0
                for i in range(len(s)):
                    if (s[i] < s[m_i] and r[i] == -1) or r[m_i] != -1:
                        m_i = i
                cnt += 1
                r[m_i] = cnt
            return r

        return sample_correlation_coefficients.pearson([ranging(samples[0]), ranging(samples[1])])