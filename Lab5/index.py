import math
from Lab5.experiments import *


if __name__ == "__main__":
    for exp in [
        simple_dist_test,
        complex_dist_test,
        ellipse_test
    ]:
        for cap in [20, 60, 100]:
            exp(cap)
