import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R
from scipy.integrate import cumulative_trapezoid as cumtrapz
import matplotlib.pyplot as plt

OBJECT = 'A'
RUN = 1

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
    peak = np.argmax(velocity)
    baseline = np.median(velocity[(peak - 350):(peak - 250)])
    slope = velocity[peak] - baseline

    low = baseline + slope * 0.2
    high = baseline + slope * 0.8

    i_lo, i_hi = 0, 0

    for i in range(peak):
        if velocity[i] <= low:
            i_lo = i
        if velocity[i] <= high:
            i_hi = i

    plt.plot(time, velocity, label="Velocity", color="blue", linewidth=1)
    plt.plot(time[i_lo:i_hi], velocity[i_lo:i_hi], label="Constant Accel. Phase (20-80% of Descent)", color="red", linewidth=2)
    plt.legend()
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
    high = baseline + slope * 0.8

    i_lo, i_hi = 0, 0

    for i in range(peak):
        if velo[i] <= low:
            i_lo = i
        if velo[i] <= high:
            i_hi = i

    ramp_t, ramp_v = [], []

    for i in range(i_lo, i_hi):
        ramp_t.append(time[i])
        ramp_v.append(velo[i])

    return np.polyfit(ramp_t, ramp_v, 1)[0]

def output_baro_drop_aligned_accel_values(vt):
    # ONLY USE FOR A 1
    velo, time = vt
    Baro = pd.read_csv(PATH + "data/Obj-" + OBJECT + "-Runs/" + str(RUN) + "/Barometer.csv", index_col='time')
    lo, hi = 53.665540039, 61.07724951
    baseline = np.median(velo[(time > 49) & (time < 53)])
    baro_window = Baro[(Baro['seconds_elapsed'] >= lo) & (Baro['seconds_elapsed'] <= hi)]
    print("time_s, altitude_m, velocity_ms")

    for _, row in baro_window.iterrows():
        time_smpl = row['seconds_elapsed']
        near_baro_time = (time >= time_smpl - 0.5) & (time <= time_smpl + 0.5)
        v = velo[near_baro_time].mean() - baseline
        print(round(time_smpl, 1), round(row['relativeAltitude'], 3), round(v, 3), sep=", ")


if __name__ == '__main__':
    output_baro_drop_aligned_accel_values(integrate()) # output graph values
    exit(0)
    for i in ['A', 'B']:
        OBJECT = i
        for j in [1, 2, 3, 4, 5]:
            RUN = j
            ACCEL = pd.read_csv(PATH + "data/Obj-" + OBJECT + "-Runs/" + str(RUN) + "/Accelerometer.csv", index_col='time')
            ORIENT = pd.read_csv(PATH + "data/Obj-" + OBJECT + "-Runs/" + str(RUN) + "/Orientation.csv", index_col='time')
            # print(i + str(j) + " " + str(find_slope_midsect(integrate()))) # Calculates acceleraton over ideal period
            # graph(integrate()) # Graphs velocity
