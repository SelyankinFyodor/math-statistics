import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd


def butter_filter(input_, cutoff, fs, btype, order=5):
    """
    Applies Butterworth filter
    """

    b, a = signal.butter(order, cutoff / (0.5 * fs), btype=btype, analog=False)
    return signal.filtfilt(b, a, input_)


def remove_emissions(x_arr, y_arr, em_border):
    """
    :param x_arr:
    :param y_arr:
    :param em_border:array of intervals
    :return: source x_arr y_arr with em_border cuts
    """
    if len(em_border) == 0:
        return x_arr, y_arr

    x_n, y_n = [], []
    current_segment = 0
    for x, y in zip(x_arr, y_arr):
        if em_border[current_segment][1] < x and len(em_border)-1 > current_segment:
            current_segment += 1
        if not em_border[current_segment][0] < x < em_border[current_segment][1]:
            x_n.append(x)
            y_n.append(y)
    return x_n, y_n


def moving_average(x, w):
    """
    Applies moving average window
    """

    return np.convolve(x, np.ones(w), "valid") / w


def get_valid_freq(signal_from_sht, roi, emissions):
    """
    :param signal_from_sht: array read from .sht file
    :param roi: region of interest for the signal
    :param emissions: array of region of emission
    :return: array of time periods and array of frequencies
    """

    high_pass_cutoff = 250
    low_pass_cutoff = 2000
    moving_average_window_size = 5

    data = np.array((signal_from_sht.get_data_x(), signal_from_sht.get_data_y()))
    x = data[0, roi[0]:roi[1]]
    y = data[1, roi[0]:roi[1]]
    sample_rate = 1.0 / (x[1] - x[0])
    y = butter_filter(y, high_pass_cutoff, sample_rate, btype="high")
    y = butter_filter(y, low_pass_cutoff, sample_rate, btype="low")
    up_border = np.percentile(y, 90)
    down_border = np.percentile(y, 10)
    vld_ind = []
    for i in range(len(y)):
        if not down_border < y[i] < up_border:
            vld_ind.append(i)
    zero_crossings = np.where(np.diff(np.sign(y)))[0]
    freqs = [1 / (x[zero_crossings[i + 2]] - x[zero_crossings[i]]) for i in range(len(zero_crossings) - 2)]
    x = [x[i] for i in zero_crossings]
    x = x[:-(moving_average_window_size + 1)]
    y = moving_average(freqs, moving_average_window_size)
    em_coords = [[data[0][em[0]],data[0][em[1]]] for em in emissions]
    x, y = remove_emissions(x, y, em_coords)
    return x, y
