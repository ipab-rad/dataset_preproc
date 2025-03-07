#!/usr/bin/python3

# Cameras' id list
# Do not modify unless you know what you are doing!
camera_ids_list = ['fsp_l', 'rsp_l', 'lspf_r', 'lspr_l', 'rspf_l', 'rspr_r']

image_struct = {'image': {'url': ''}, 'name': ''}

# FIXME: Create all these structs from a file (see #3)

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


def get_cam_url(camera_name, cameras_list, assets_meta):

    cam_id = None
    for camera in cameras_list:
        if camera['name'] == camera_name:
            cam_id = camera['global_id']

    if cam_id is None:
        return 'S3 url not found!'

    return assets_meta[str(cam_id)]['s3_url']


def get_images(sync_key_frame, assets_meta):

    # FIXME: Simplify this (see #3)
    sample = dict()
    sample["images"] = [
        fsp_l_struct,
        rsp_l_struct,
        lspf_r_struct,
        lspr_l_struct,
        rspf_l_struct,
        rspr_r_struct,
    ]

    sample["images"][0]["url"] = get_cam_url(
        'fsp_l', sync_key_frame['cameras'], assets_meta
    )
    sample["images"][1]["url"] = get_cam_url(
        'rsp_l', sync_key_frame['cameras'], assets_meta
    )
    sample["images"][2]["url"] = get_cam_url(
        'lspf_r', sync_key_frame['cameras'], assets_meta
    )
    sample["images"][3]["url"] = get_cam_url(
        'lspr_l', sync_key_frame['cameras'], assets_meta
    )
    sample["images"][4]["url"] = get_cam_url(
        'rspf_l', sync_key_frame['cameras'], assets_meta
    )
    sample["images"][5]["url"] = get_cam_url(
        'rspr_r', sync_key_frame['cameras'], assets_meta
    )

    return sample["images"]
