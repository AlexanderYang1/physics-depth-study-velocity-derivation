import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R
from scipy.integrate import cumulative_trapezoid as cumtrapz
import matplotlib.pyplot as plt

OBJECT = 'A'
RUN = 2

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

if __name__ == "__main__":
    rotated = rotate_all()
    vertical = rotated[:, -1]
    print(vertical)
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

    plt.plot(time, velocity, label="Velocity", color="blue", linewidth=1)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Velocity over Time via Integration")
    plt.show()






