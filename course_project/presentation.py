import matplotlib.pyplot as plt
import os

current_dir = os.path.dirname(os.path.abspath(__file__))


class plot:
    """
    Plotting data and saving it to PNG file
    """

    def __init__(self, label_x="", label_y="", title="",
                 file_name='new', out_dir=os.path.join(current_dir, "output")):
        self._fig, self._subplot = plt.subplots()
        self._subplot.set_xlabel(label_x)
        self._subplot.set_ylabel(label_y)
        self._subplot.set_title(title)
        self._file_name = file_name
        self._out_dir = out_dir

    def plot(self, x, y, style="o-"):
        self._subplot.plot(x, y, style)
        return self

    def hist(self, y):
        self._subplot.hist(y, alpha=0.5, edgecolor='black', linewidth=1)
        return self

    def legend(self, legend):
        self._subplot.legend(legend)
        return self

    def show(self):
        self._fig.show()
        return self

    def xline(self, x, color='red'):
        self._subplot.axvline(x, color=color)
        return self

    def clear(self):
        self._fig.clear()
        return self


    def flush(self):
        if not os.path.exists(self._out_dir):
            os.makedirs(self._out_dir)
        out = os.path.join(self._out_dir, "%s.png" % self._file_name)
        self._fig.savefig(out)
        print("Result: %s" % out)
        return self
