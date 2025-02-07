#!/usr/bin/python3

# Pointcloud sample dictionary structure
pcd_struct = {
    "pcd": {
        "url": "pcd_url",
        "type": "pcd",
    },
    "images": [],
    "ego_pose": {
        "position": {
            "x": 0,
            "y": 0,
            "z": 0,
        },
        "heading": {
            "qx": 0,
            "qy": 0,
            "qz": 0,
            "qw": 1,
        },
    },
    "default_z": "-1.78",  # Top lidar height from ground level
    "name": "test",
    "timestamp": 0,
}
