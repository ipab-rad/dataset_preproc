#!/usr/bin/python3

import warnings  # To ignore FutureWarning from pandas

warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd

# Front camera dictionary structure
fsp_l_struct = {
    "url": "image_url",
    "row": 0,  # Row when displaying multiple camera images
    "col": 1,  # Col when displaying multiple camera images
    "intrinsics": {
        "intrinsic_matrix": [
            [1451.49531, 0.0, 1218.93228],
            [0.0, 1450.7118, 683.50771],
            [0.0, 0.0, 1.0],
        ]
    },
    "extrinsics": {
        "translation": {"x": 0.660, "y": 0.316, "z": -0.275},
        "rotation": {"qx": 0.518, "qy": -0.515, "qz": 0.486, "qw": -0.480},
    },
    "distortion": {
        "model": "brown-conrady",
        "coefficients": {
            "k1": -0.01423,
            "k2": 0.03806,
            "k3": 0.0,
            "p1": -0.00111,
            "p2": 0.00149,
        },
    },
    "camera_convention": "OpenCV",
    "name": "camera_fsp_l",
}

# Front camera dictionary structure
rsp_l_struct = {
    "url": "image_url",
    "row": 1,  # Row when displaying multiple camera images
    "col": 1,  # Col when displaying multiple camera images
    "intrinsics": {
        "intrinsic_matrix": [
            [1453.84541, 0.0, 1196.47476],
            [0.0, 1452.87508, 674.82694],
            [0.0, 0.0, 1.0],
        ]
    },
    "extrinsics": {
        "translation": {"x": -0.530, "y": -0.282, "z": -0.217},
        "rotation": {"qx": 0.523, "qy": 0.526, "qz": -0.475, "qw": -0.474},
    },
    "distortion": {
        "model": "brown-conrady",
        "coefficients": {
            "k1": -0.01765,
            "k2": 0.04014,
            "k3": 0.0,
            "p1": -0.00211,
            "p2": 0.00385,
        },
    },
    "camera_convention": "OpenCV",
    "name": "camera_rsp_l",
}

# Front camera dictionary structure
lspf_r_struct = {
    "url": "image_url",
    "row": 0,  # Row when displaying multiple camera images
    "col": 0,  # Col when displaying multiple camera images
    "intrinsics": {
        "intrinsic_matrix": [
            [1444.38913, 0.0, 1162.88551],
            [0.0, 1442.8811, 716.39319],
            [0.0, 0.0, 1.0],
        ]
    },
    "extrinsics": {
        "translation": {"x": 0.011, "y": 0.557, "z": -0.224},
        "rotation": {"qx": -0.723, "qy": 0.149, "qz": -0.143, "qw": 0.659},
    },
    "distortion": {
        "model": "brown-conrady",
        "coefficients": {
            "k1": -0.02565,
            "k2": 0.04315,
            "k3": 0.0,
            "p1": 0.00124,
            "p2": 0.00201,
        },
    },
    "camera_convention": "OpenCV",
    "name": "camera_lspf_r",
}

# Front camera dictionary structure
lspr_l_struct = {
    "url": "image_url",
    "row": 1,  # Row when displaying multiple camera images
    "col": 0,  # Col when displaying multiple camera images
    "intrinsics": {
        "intrinsic_matrix": [
            [1465.059, 0.0, 1171.9781],
            [0.0, 1464.79803, 666.8666],
            [0.0, 0.0, 1.0],
        ]
    },
    "extrinsics": {
        "translation": {"x": -0.324, "y": 0.513, "z": -0.224},
        "rotation": {"qx": -0.722, "qy": -0.161, "qz": 0.140, "qw": 0.658},
    },
    "distortion": {
        "model": "brown-conrady",
        "coefficients": {
            "k1": -0.03082,
            "k2": 0.0505,
            "k3": 0.0,
            "p1": -0.00112,
            "p2": 0.00179,
        },
    },
    "camera_convention": "OpenCV",
    "name": "camera_lspr_l",
}

# Front camera dictionary structure
rspf_l_struct = {
    "url": "image_url",
    "row": 0,  # Row when displaying multiple camera images
    "col": 2,  # Col when displaying multiple camera images
    "intrinsics": {
        "intrinsic_matrix": [
            [1461.55571, 0.0, 1224.79388],
            [0.0, 1460.11652, 698.92044],
            [0.0, 0.0, 1.0],
        ]
    },
    "extrinsics": {
        "translation": {"x": 0.032, "y": -0.523, "z": -0.214},
        "rotation": {"qx": -0.149, "qy": 0.719, "qz": -0.663, "qw": 0.149},
    },
    "distortion": {
        "model": "brown-conrady",
        "coefficients": {
            "k1": -0.02165,
            "k2": 0.04774,
            "k3": 0.0,
            "p1": -0.00045,
            "p2": -0.00174,
        },
    },
    "camera_convention": "OpenCV",
    "name": "camera_rspf_l",
}

# Front camera dictionary structure
rspr_r_struct = {
    "url": "image_url",
    "row": 1,  # Row when displaying multiple camera images
    "col": 2,  # Col when displaying multiple camera images
    "intrinsics": {
        "intrinsic_matrix": [
            [1447.00739, 0.0, 1213.12424],
            [0.0, 1447.20673, 686.80094],
            [0.0, 0.0, 1.0],
        ]
    },
    "extrinsics": {
        "translation": {"x": -0.329, "y": -0.551, "z": -0.214},
        "rotation": {"qx": 0.162, "qy": 0.723, "qz": -0.659, "qw": -0.134},
    },
    "distortion": {
        "model": "brown-conrady",
        "coefficients": {
            "k1": -0.02134,
            "k2": 0.04395,
            "k3": 0.0,
            "p1": -0.00182,
            "p2": 0.0,
        },
    },
    "camera_convention": "OpenCV",
    "name": "camera_rspr_r",
}

# Load the TUM trajectory file
fsp_l_path = "/opt/ros_ws/output/Test_3D_3_fsp_l.txt"
rsp_l_path = "/opt/ros_ws/output/Test_3D_3_rsp_l.txt"
lspf_r_path = "/opt/ros_ws/output/Test_3D_3_lspf_r.txt"
lspr_l_path = "/opt/ros_ws/output/Test_3D_3_lspr_l.txt"
rspf_l_path = "/opt/ros_ws/output/Test_3D_3_rspf_l.txt"
rspr_r_path = "/opt/ros_ws/output/Test_3D_3_rspr_r.txt"
columns = ['url']

# Read text file
fsp_l_file = pd.read_csv(fsp_l_path, delim_whitespace=True, header=None, names=columns)
rsp_l_file = pd.read_csv(rsp_l_path, delim_whitespace=True, header=None, names=columns)
lspf_r_file = pd.read_csv(lspf_r_path, delim_whitespace=True, header=None, names=columns)
lspr_l_file = pd.read_csv(lspr_l_path, delim_whitespace=True, header=None, names=columns)
rspf_l_file = pd.read_csv(rspf_l_path, delim_whitespace=True, header=None, names=columns)
rspr_r_file = pd.read_csv(rspr_r_path, delim_whitespace=True, header=None, names=columns)


fsp_l_urls = fsp_l_file['url'].tolist()
rsp_l_urls = rsp_l_file['url'].tolist()
lspf_r_urls = lspf_r_file['url'].tolist()
lspr_l_urls = lspr_l_file['url'].tolist()
rspf_l_urls = rspf_l_file['url'].tolist()
rspr_r_urls = rspr_r_file['url'].tolist()

def getImages(i):
    sample = dict()
    sample["images"] = [fsp_l_struct, rsp_l_struct, lspf_r_struct, lspr_l_struct, rspf_l_struct, rspr_r_struct]
    sample["images"][0]["url"] = fsp_l_urls[i]
    sample["images"][1]["url"] = rsp_l_urls[i]
    sample["images"][2]["url"] = lspf_r_urls[i]
    sample["images"][3]["url"] = lspr_l_urls[i]
    sample["images"][4]["url"] = rspf_l_urls[i]
    sample["images"][5]["url"] = rspr_r_urls[i]
    return sample["images"]