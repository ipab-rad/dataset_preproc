#!/usr/bin/python3

sensor_sequence_struct = {'name': '', 'task_type': '', 'attributes': {}}

# Pointcloud sample dictionary structure
pcd_struct = {
    'pcd': {
        'url': 'pcd_url',
        'type': 'pcd',
    },
    'images': [],
    'ego_pose': {
        'position': {
            'x': 0,
            'y': 0,
            'z': 0,
        },
        'heading': {
            'qx': 0,
            'qy': 0,
            'qz': 0,
            'qw': 1,
        },
    },
    'default_z': 0,
    'name': 'test',
    'timestamp': 0,
}
