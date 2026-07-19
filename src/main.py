import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R

OBJECT = 'A'
RUN = 1

ACCEL = pd.read_csv("data/Obj-" + OBJECT + "-Runs/" + str(RUN) + "/Accelerometer.csv", index_col='time')
ORIENT = pd.read_csv("data/Obj-" + OBJECT + "-Runs/" + str(RUN) + "/Orientation.csv", index_col='time')


def rotate(vec: np.ndarray, quat: np.ndarray) -> np.ndarray:
    rotation = R.from_quat(quat)
    rotated_accel = rotation.apply(vec)
    return rotated_accel


def rotate_all():
    row_count = len(ACCEL) # noqa
    for i in range(row_count):
        accel_vec = ACCEL[['x', 'y', 'z']].iloc[i].to_numpy()
        orient_q = ORIENT[['qw', 'qx', 'qy', 'qz']].iloc[i].to_numpy()
        rotate(accel_vec, orient_q)

if __name__ == "__main__":
    rotate_all()


