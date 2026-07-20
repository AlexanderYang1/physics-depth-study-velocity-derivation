import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R
from scipy.integrate import cumulative_trapezoid as cumtrapz
import matplotlib.pyplot as plt

OBJECT = 'B'
RUN = 5

PATH = "/Users/alexanderyang/Documents/Main Directory/Programming/physics-depth-study-velocity-derivation/"
ACCEL = pd.read_csv(PATH + "data/Obj-" + OBJECT + "-Runs/" + str(RUN) + "/Accelerometer.csv", index_col='time')
ORIENT = pd.read_csv(PATH + "data/Obj-" + OBJECT + "-Runs/" + str(RUN) + "/Orientation.csv", index_col='time')

def rotate(vec: np.ndarray, quat: np.ndarray) -> np.ndarray:
    rotation = R.from_quat(quat)
    rotated_accel = rotation.apply(vec)
    return rotated_accel

def rotate_all():
    row_count = len(ACCEL) # noqa
    rotated_list = []

    for i in range(row_count):
        accel_vec = ACCEL[['x', 'y', 'z']].iloc[i].to_numpy()
        orient_q = ORIENT[['qx', 'qy', 'qz', 'qw']].iloc[i].to_numpy()
        rotated_accel = rotate(accel_vec, orient_q)
        rotated_list.append(rotated_accel)

    return np.array(rotated_list)

def integrate():
    rotated = rotate_all()
    vertical = rotated[:, -1]
    # print(vertical)
    velocity = cumtrapz(vertical) * 0.01

    v_t_table = []

    i = 0
    for j in velocity:
        arr =[i * 0.01, j]
        v_t_table.append(arr)
        i += 1

    v_t_table = np.array(v_t_table)
    time = v_t_table[:, 0]
    velocity = v_t_table[:, 1]
    return velocity, time

def graph(vt):
    velocity, time = vt
    plt.plot(time, velocity, label="Velocity", color="blue", linewidth=1)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Downwards Velocity over Time")
    plt.savefig(PATH + "out/run-" + OBJECT + str(RUN))
    plt.show()

# Go to middle of slope and fetch gradient
def find_slope_midsect(vt):
    velo, time = vt
    diff = np.diff(velo)
    peak = np.argmax(velo)
    baseline = np.median(velo[(peak - 350):(peak - 250)])
    slope = velo[peak] -  baseline

    low = baseline + slope * 0.2
    high = baseline + slope * 0.9

    i_lo, i_hi = 0, 0

    for i in range(peak):
        if velo[i] <= low:
            i_lo = i
        if velo[i] >= high:
            i_hi = i

    ramp_t, ramp_v = [], []

    for i in range(i_lo, i_hi):
        ramp_t.append(time[i])
        ramp_v.append(velo[i])

    return np.polyfit(ramp_t, ramp_v, 1)[0]

if __name__ == '__main__':
    for i in ['A', 'B']:
        OBJECT = i
        for j in [1, 2, 3, 4, 5]:
            RUN = j
            ACCEL = pd.read_csv(PATH + "data/Obj-" + OBJECT + "-Runs/" + str(RUN) + "/Accelerometer.csv", index_col='time')
            ORIENT = pd.read_csv(PATH + "data/Obj-" + OBJECT + "-Runs/" + str(RUN) + "/Orientation.csv", index_col='time')
            # print(i + str(j) + " " + str(find_slope_midsect(integrate()))) # Calculates acceleraton over ideal period
            graph(integrate()) # Graphs velocity
