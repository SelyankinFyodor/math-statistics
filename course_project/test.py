import sys
import os
from course_project import ripper
import matplotlib.pyplot as plt


current_dir = os.path.dirname(os.path.abspath(__file__))
PYGLOBUS_ROOT = os.path.join(current_dir, "pyglobus", "python")
# PYGLOBUS_ROOT = r'C:\workspace\poly\math-statistics\course_project\pyglobus\python'
PATH_TO_SHT_FILE = r'C:\workspace\poly\math-statistics\course_project\shts\sht38516.sht'
SHT_NUMBER = 38516
NUM_SIGNAL = 26

sys.path.append(PYGLOBUS_ROOT)
try:
    import pyglobus
except ImportError as e:
    print("Cannot import pyglobus from %s, exiting" % PYGLOBUS_ROOT)
    sys.exit(1)


# 1. Read using pyglobus

sht_reader = pyglobus.util.ShtReader(PATH_TO_SHT_FILE)

signal = sht_reader.get_signal(NUM_SIGNAL)

x, y = signal.get_data_x(), signal.get_data_y()

plt.figure()
plt.plot(x, y)

# 2. Read using ripper

data_all = ripper.extract("shts", SHT_NUMBER, [NUM_SIGNAL])

x, y = ripper.x_y(data_all[0][NUM_SIGNAL])

plt.figure()
plt.plot(x, y)

plt.show()