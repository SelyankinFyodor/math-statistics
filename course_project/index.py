import numpy as np
import os
import sys
import json
from course_project.sawtooth_detection import getRoi
from course_project.sawtooth_frequency_computation import get_valid_freq
from course_project.presentation import plot
import pandas as pd


current_dir = os.path.dirname(os.path.abspath(__file__))
pyglobus_dir = os.path.join(current_dir, "pyglobus", "python")
sht_dir = os.path.join(current_dir, "sht")

sys.path.append(pyglobus_dir)
try:
    import pyglobus
except ImportError as e:
    print("Cannot import pyglobus from %s, exiting" % pyglobus_dir)
    sys.exit(1)


def main1():
    """
    sawtooth detection
    """

    with open("VALID_DATA.json") as json_file:
        valid_data = json.load(json_file)

    out_sawtooth_detection = os.path.join(current_dir, "output", "sawtooth_detection")
    for sht_file in valid_data:
        for s in valid_data[sht_file]["signals"]:
            sht_reader = pyglobus.util.ShtReader(os.path.join(sht_dir, "%s.sht" % sht_file))
            signal_from_sht = sht_reader.get_signal(int(s))
            data = np.array((signal_from_sht.get_data_x(), signal_from_sht.get_data_y()))
            x, y, start, end = getRoi(data)
            print("%i, %i" % (start, end))


def comparing_in_row():
    """
    sawtooth frequency compering
    """

    with open("VALID_DATA.json") as json_file:
        data = json.load(json_file)
    out_joint_freq = os.path.join(current_dir, "output", "joint_frequency_graph")
    sht_file = 'sht38515'
    freq_data = {}
    legend_label = []
    freq_plot = plot("Время, с", "Частота, Гц",
                     "Совместный график частот для %s" % sht_file,
                     "joint_frequency_graph_%s" % sht_file, out_joint_freq)
    for s in data[sht_file]["signals"]:
        legend_label.append(s)
        x, y = get_valid_freq(
            pyglobus.util.ShtReader(os.path.join(sht_dir, "%s.sht" % sht_file)).get_signal(int(s)),
            data[sht_file]["signals"][s], data[sht_file]["emissions"])
        freq_data[s] = y
        freq_plot.plot(x, y, 'o-')
    freq_plot.legend(legend_label)
    freq_plot.flush()
    df = pd.DataFrame(freq_data, columns=[s for s in data[sht_file]["signals"]])
    freq_hist = plot("Частота, Гц", "частота частот",
                     "Совместная гистограмма частот для %s" % sht_file,
                     "joint_frequency_hist_%s" % sht_file, out_joint_freq)
    for y_s in freq_data:
        freq_hist.hist(freq_data[y_s])
    freq_hist.legend(legend_label)
    freq_hist.flush()
    cm = df.corr()
    print(cm)


def comparing_in_column():
    with open("VALID_DATA.json") as json_file:
        data = json.load(json_file)
    res_sign = 20
    freq_data = {}
    out_joint_freq = os.path.join(current_dir, "output", "joint_frequency_graph")
    legend_label = []
    freq_plot = plot("Время, с", "Частота, Гц",
                     "Совместный график частот для %i сигнала" % res_sign,
                     "joint_frequency_graph_sign_%s" % res_sign, out_joint_freq)
    res_sht = [
        'sht38515',
        'sht38516',
        'sht38873',
        'sht38875',
        'sht38876',
        'sht38892',
    ]
    for sht_file in res_sht:
        legend_label.append(sht_file)
        x, y = get_valid_freq(
            pyglobus.util.ShtReader(os.path.join(sht_dir, "%s.sht" % sht_file)).get_signal(res_sign),
            data[sht_file]["signals"][str(res_sign)], data[sht_file]["emissions"])
        freq_data[sht_file] = y
        freq_plot.plot(x, y, 'o-')
    freq_plot.legend(legend_label)
    freq_plot.flush()
    df = pd.DataFrame(freq_data, columns=res_sht)
    freq_hist = plot("Частота, Гц", "частота частот",
                     "Совместная гистограмма частот для %s сигнала" % res_sign,
                     "joint_frequency_hist_sign_%s" % res_sign, out_joint_freq)
    for y_s in freq_data:
        freq_hist.hist(freq_data[y_s])
    freq_hist.legend(legend_label)
    freq_hist.flush()
    cm = df.corr()
    print(cm)


if __name__ == "__main__":
    comparing_in_row()
    comparing_in_column()
