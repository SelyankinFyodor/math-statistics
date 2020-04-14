import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import signal
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(current_dir, "output", "sawtooth_detection")
pyglobus_root = os.path.join(current_dir, "pyglobus", "python")

sht_path = os.path.join(current_dir, "sht")
sht_files = [
    os.path.join(sht_path, "sht38515.sht"),
    os.path.join(sht_path, "sht38516.sht"),
    os.path.join(sht_path, "sht38851.sht"),
    os.path.join(sht_path, "sht38852.sht"),
    os.path.join(sht_path, "sht38866.sht"),
    os.path.join(sht_path, "sht38867.sht")
]

# костыли для нормального определения границ пил
SAWTOOTH_ROI = {
    'sht38515': [162000, 197700]
}

num_signal = [18, 19, 20, 26, 55]

SIGNAL_SAMPLING_RATE = int(1e6)
HIGH_PASS_CUTOFF = 400
SMOOTHED_DD1_ORDER = 30
LOW_PASS_CUTOFF = 5000
SAWTOOTH_DETECTION_THRESHOLD = 0.0005
ROI_DETECTOR_MEAN_SCALE = 1
MOVING_AVERAGE_WINDOW_SIZE = 5

sys.path.append(pyglobus_root)
try:
    import pyglobus
except ImportError as e:
    print("Cannot import pyglobus from %s, exiting" % pyglobus_root)
    sys.exit(1)


stage = 0


def getRoi(data_from_sht):
    roi = pyglobus.sawtooth.get_signal_roi(data_from_sht[1], mean_scale=1)
    x = np.copy(data_from_sht[0, roi[0]:roi[1]])
    y = np.copy(data_from_sht[1, roi[0]:roi[1]])
    pyglobus.dsp.high_pass_filter(y, HIGH_PASS_CUTOFF, SIGNAL_SAMPLING_RATE)
    y = pyglobus.dsp.first_order_diff_filter(y, SMOOTHED_DD1_ORDER)
    y = np.abs(y)
    pyglobus.dsp.low_pass_filter(y, LOW_PASS_CUTOFF, SIGNAL_SAMPLING_RATE)
    start_ind, end_ind = pyglobus.sawtooth.get_sawtooth_indexes(y, SAWTOOTH_DETECTION_THRESHOLD)
    return x,y,start_ind, end_ind


# Plotting sample_data and saving it to PNG file
def plot(x, y, label_x, label_y, color="k", new_fig=True, flush=True):
    global stage

    if new_fig:
        plt.figure(figsize=(15, 10))

    plt.plot(x, y, color)
    plt.xlabel(label_x, fontsize=25)
    plt.ylabel(label_y, fontsize=25)

    if flush:
        out = os.path.join(output_dir, "#%i.png" % stage)
        plt.savefig(out)

        print("Stage %i result:" % stage, out)

        stage += 1


# Applies Butterworth filter
def butter_filter(input_, cutoff, fs, btype, order=5):
    b, a = signal.butter(order, cutoff / (0.5 * fs), btype=btype, analog=False)
    return signal.filtfilt(b, a, input_)


# Applies moving average window
def moving_average(x, w):
    return np.convolve(x, np.ones(w), "valid") / w


# def main1():
#     font = {"size": 22}
#
#     plt.rc("font", **font)
#
#     os.makedirs(output_dir, exist_ok=True)
#
#     print("Stage %i: Data loading" % stage)
#
#     sht_reader = pyglobus.util.ShtReader(sht_files[1])
#     signal = sht_reader.get_signal(num_signal[3])
#     data = np.array((signal.get_data_x(), signal.get_data_y()))
#
#     print("Loaded %s" % sht_files[0])
#
#     plot(data[0], data[1], "Время, с", "U, В")
#
#     print("Stage %i: ROI extracting" % stage)
#
#     roi = pyglobus.sawtooth.get_signal_roi(data[1], mean_scale=1)
#     x = np.copy(data[0, roi[0]:roi[1]])
#     y = np.copy(data[1, roi[0]:roi[1]])
#
#     plot(x, y, "Время, с", "U, В")
#
#     print("Stage %i: High pass filtering" % stage)
#
#     pyglobus.dsp.high_pass_filter(y, HIGH_PASS_CUTOFF, SIGNAL_SAMPLING_RATE)
#
#     plot(x, y, "Время, с", "U, В")
#
#     print("Stage %i: Smoothed differentiation" % stage)
#
#     y = pyglobus.dsp.first_order_diff_filter(y, SMOOTHED_DD1_ORDER)
#
#     plot(x, y, "Время, с", "U', В/с")
#
#     print("Stage %i: Taking absolute value" % stage)
#
#     y = np.abs(y)
#
#     plot(x, y, "Время, с", "|U'|, В/с")
#
#     print("Stage %i: Low pass filtering" % stage)
#
#     pyglobus.dsp.low_pass_filter(y, LOW_PASS_CUTOFF, SIGNAL_SAMPLING_RATE)
#
#     plot(x, y, "Время, с", "|U'|, В/с", flush=False)
#
#     plot(x, [SAWTOOTH_DETECTION_THRESHOLD] * len(x), "Время, с", "|U'|, В/с", color="r", new_fig=False)
#
#     print("Stage %i: Sawtooth detection" % stage)
#
#     start_ind, end_ind = pyglobus.sawtooth.get_sawtooth_indexes(y, SAWTOOTH_DETECTION_THRESHOLD)
#     print("start_ind: %i, end_ind %i" % (start_ind, end_ind))
#
#     plt.figure(figsize=(15, 10))
#     plt.axvline(x[start_ind], color="r")
#     plt.axvline(x[end_ind], color="r")
#     plot(data[0], data[1], "Время, с", "U, В", new_fig=False)
#
#     print("Done!")


# def main2():
#     font = {"size": 22}
#
#     plt.rc("font", **font)
#
#     os.makedirs(output_dir, exist_ok=True)
#
#     print("Stage %i: Data loading and preparing" % stage)
#
#     data = np.load(os.path.join(current_dir, "sample_data", DATA_FILE))
#
#     print("Loaded %s" % DATA_FILE)
#
#     x = data[0, SAWTOOTH_ROI[0]:SAWTOOTH_ROI[1]]
#     y = data[1, SAWTOOTH_ROI[0]:SAWTOOTH_ROI[1]]
#
#     plot(data[0], data[1], "Время, с", "U, В")
#
#     print("Stage %i: High pass filtering" % stage)
#
#     sample_rate = 1.0 / (x[1] - x[0])
#
#     y = butter_filter(y, HIGH_PASS_CUTOFF, sample_rate, btype="high")
#
#     plot(x, y, "Время, с", "U, В")
#
#     print("Stage %i: Low pass filtering" % stage)
#
#     y = butter_filter(y, LOW_PASS_CUTOFF, sample_rate, btype="low")
#
#     plot(x, y, "Время, с", "U, В")
#
#     print("Stage %i: Finding zero crossings" % stage)
#
#     zero_crossings = np.where(np.diff(np.sign(y)))[0]
#
#     plot(x, y, "Время, с", "U, В", flush=False)
#     plot(x[zero_crossings], y[zero_crossings], "Время, с", "U, В", color="rx", new_fig=False)
#
#     print("Stage %i: Computing frequencies" % stage)
#
#     freqs = [1 / (x[zero_crossings[i + 2]] - x[zero_crossings[i]]) for i in range(len(zero_crossings) - 2)]
#
#     x = x[zero_crossings][:-(MOVING_AVERAGE_WINDOW_SIZE + 1)]
#     y = moving_average(freqs, MOVING_AVERAGE_WINDOW_SIZE)
#
#     plot(x, y, "Время, с", "Частота, Гц", color="ko-")
#
#     print("Done!")


if __name__ == "__main__":
    sht_reader = pyglobus.util.ShtReader(sht_files[5])
    signal_from_sht = sht_reader.get_signal(num_signal[2])
    data = np.array((signal_from_sht.get_data_x(), signal_from_sht.get_data_y()))
    x,y,start, end = getRoi(data)
    plt.figure(figsize=(15, 10))
    plt.axvline(x[start], color="r")
    plt.axvline(x[end], color="r")
    plot(data[0], data[1], "Время, с", "U, В", new_fig=False)
