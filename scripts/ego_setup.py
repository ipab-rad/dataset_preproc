#!/usr/bin/python3

import warnings  # To ignore FutureWarning from pandas

warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd

# Load the TUM trajectory file
file_path = "/opt/ros_ws/output/2024_11_15-14_05_41_meadows_new_antennas_galileo_44_trajectory.tum"
columns = ['timestamp', 'x', 'y', 'z', 'qx', 'qy', 'qz', 'qw']

# Read text file
df = pd.read_csv(file_path, delim_whitespace=True, header=None, names=columns)

# Store the data into separate lists
ego_x = df['x'].tolist()
ego_y = df['y'].tolist()
ego_z = df['z'].tolist()
ego_qx = df['qx'].tolist()
ego_qy = df['qy'].tolist()
ego_qz = df['qz'].tolist()
ego_qw = df['qw'].tolist()


def getEgoPose(i):
    ego_pose = dict()
    ego_pose["position"] = {"x": ego_x[i], "y": ego_y[i], "z": ego_z[i]}
    ego_pose["heading"] = {
        "qx": ego_qx[i],
        "qy": ego_qy[i],
        "qz": ego_qz[i],
        "qw": ego_qw[i],
    }
    return ego_pose
