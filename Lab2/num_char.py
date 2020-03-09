class numerical_characteristics:
    @staticmethod
    def sample_mean(sample):
        return sum(sample)/len(sample)

    @staticmethod
    def median(sample):
        return sample[len(sample) // 2] if len(sample) % 2 == 1 \
            else (sample[len(sample) // 2 - 1] + sample[len(sample) // 2]) / 2

    @staticmethod
    def halfsum_extreme(sample):
        return (sample[0] + sample[len(sample) - 1]) / 2

    @staticmethod
    def halfsum_quartile(sample):
        def quartile(p):
            return sample[len(sample) * p - 1] if int(len(sample) * p) == len(sample) \
                else sample[int((len(sample) * p)) - 1]
        return (quartile(1/4) + quartile(3/4)) / 2

    @staticmethod
    def truncated_mean(sample):
        return sum(sample[len(sample) // 4: len(sample) - len(sample) // 4]) / (len(sample) - 2 * len(sample) // 4)

    @staticmethod
    def dispersion_def(sample):
        e = numerical_characteristics.sample_mean(sample)
        return sum(list(map(lambda x: (x-e)**2, sample))) / len(sample)

    @staticmethod
    def dispersion_exp(sample):
        return numerical_characteristics.sample_mean(list(map(lambda x: x*x, sample))) \
               - (numerical_characteristics.sample_mean(sample))**2

