import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import signal
import sys
import json
from course_project.sawtooth_detect import getRoi


current_dir = os.path.dirname(os.path.abspath(__file__))
out_sawtooth_detection = os.path.join(current_dir, "output", "sawtooth_detection")
out_freq_comp = os.path.join(current_dir, "output", "sawtooth_frequency_computation")
pyglobus_dir = os.path.join(current_dir, "pyglobus", "python")
sht_dir = os.path.join(current_dir, "sht")

sys.path.append(pyglobus_dir)
try:
    import pyglobus
except ImportError as e:
    print("Cannot import pyglobus from %s, exiting" % pyglobus_dir)
    sys.exit(1)


def plot(x, y, label_x, label_y, color="k", new_fig=True, flush=True, name='new', out_dir=os.path.join(current_dir, "output")):
    """Plotting sample_data and saving it to PNG file"""

    if new_fig:
        plt.figure(figsize=(15, 10))
    plt.plot(x, y, color)
    plt.xlabel(label_x, fontsize=25)
    plt.ylabel(label_y, fontsize=25)
    if flush:
        out = os.path.join(out_dir, "%s.png" % name)
        plt.savefig(out)
        print("Result: %s" % out)


def butter_filter(input_, cutoff, fs, btype, order=5):
    """Applies Butter worth filter"""

    b, a = signal.butter(order, cutoff / (0.5 * fs), btype=btype, analog=False)
    return signal.filtfilt(b, a, input_)


def moving_average(x, w):
    """Applies moving average window"""

    return np.convolve(x, np.ones(w), "valid") / w


def main1():
    """returns areas of interest for all combinations from valid_data"""

    with open("VALID_DATA.json") as json_file:
        valid_data = json.load(json_file)
    for el in valid_data:
        for s in valid_data[el]:
            sht_reader = pyglobus.util.ShtReader(os.path.join(sht_dir, "%s.sht" % el))
            signal_from_sht = sht_reader.get_signal(int(s))
            data = np.array((signal_from_sht.get_data_x(), signal_from_sht.get_data_y()))
            x, y, start, end = getRoi(data)
            plt.axvline(data[0][valid_data[el][s][0]], color="r")
            plt.axvline(data[0][valid_data[el][s][1]], color="b")
            plot(data[0], data[1], "Время, с", "U, В", new_fig=False, name="%s_%s" % (el, s), out_dir=out_sawtooth_detection)
            plt.clf()


if __name__ == "__main__":
    main1()
