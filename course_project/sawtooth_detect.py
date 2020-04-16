import os
import sys
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
pyglobus_dir = os.path.join(current_dir, "pyglobus", "python")
sys.path.append(pyglobus_dir)
try:
    import pyglobus
except ImportError as e:
    print("Cannot import pyglobus from %s, exiting" % pyglobus_dir)
    sys.exit(1)


def getRoi(data_from_sht):
    """gives an approximate position of the area of ​​interest"""

    high_pass_cutoff = 400
    low_pass_cutoff = 5000
    smoothed_dd1_order = 30
    sawtooth_detection_threshold = 0.0005
    signal_sampling_rate = int(1e6)

    roi = pyglobus.sawtooth.get_signal_roi(data_from_sht[1], mean_scale=1)
    x = np.copy(data_from_sht[0, roi[0]:roi[1]])
    y = np.copy(data_from_sht[1, roi[0]:roi[1]])
    pyglobus.dsp.high_pass_filter(y, high_pass_cutoff, signal_sampling_rate)
    y = pyglobus.dsp.first_order_diff_filter(y, smoothed_dd1_order)
    y = np.abs(y)
    pyglobus.dsp.low_pass_filter(y, low_pass_cutoff, signal_sampling_rate)
    start_ind, end_ind = pyglobus.sawtooth.get_sawtooth_indexes(y, sawtooth_detection_threshold)
    return x, y, start_ind+roi[0], end_ind+roi[0]