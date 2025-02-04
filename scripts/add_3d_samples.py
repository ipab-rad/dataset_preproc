#!/usr/bin/python3

import sys
import copy
import yaml
import json
import os
from pathlib import Path
from segments import SegmentsClient

import pcd_setup, ego_setup, img_setup

# FIXME: Parametrise this in some way
dataset = 'UniversityofEdinburgh/Edinburgh_3D_Test'
seq_name = "sequence_1"


# Get Segment API key from env variable
api_key = os.getenv('SEGMENTS_API_KEY')
if not api_key:
    print(
        'ERROR: SEGMENTS_API_KEY environment variable was not found. Terminating.',
        file=sys.stderr,
    )
    sys.exit(1)

# Initialise Segments.ai client
client = SegmentsClient(api_key)

# Ensure command-line argument is provided
if len(sys.argv) < 2:
    print(
        'ERROR: Please provide the local data directory as an argument.',
        file=sys.stderr,
    )
    sys.exit(1)

# Verify provided data directory
local_data_directory = Path(sys.argv[1])
if not local_data_directory.exists():
    print(
        f'ERROR: Provided directory \'{local_data_directory}\' does not exist.',
        file=sys.stderr,
    )
    sys.exit(1)

# Load export_metadata.yaml
export_metadata_file = local_data_directory / 'export_metadata.yaml'
if not export_metadata_file.is_file():
    print(
        f'ERROR: Metadata file \'{export_metadata_file}\' not found.',
        file=sys.stderr,
    )
    sys.exit(1)

with open(export_metadata_file) as yaml_file:
    export_metadata_yaml = yaml.safe_load(yaml_file)

# Load upload_metadata.yaml
upload_metadata_file = local_data_directory / 'upload_metadata.json'
if not upload_metadata_file.is_file():
    print(
        f'ERROR: Metadata file \'{upload_metadata_file}\' not found.',
        file=sys.stderr,
    )
    sys.exit(1)

with open(upload_metadata_file) as json_file:
    upload_metadata_json = json.load(json_file)

# Search for a .tum file
tum_files = list(local_data_directory.glob('*.tum'))
if not tum_files:
    print(f'ERROR: Trajectory file (.tum ) not found.', file=sys.stderr)

print(f'Trajectory file found {tum_files[0]}')

# Initialise ego_poses based on .tum file
ego_poses = ego_setup.EgoPoses(tum_files[0])

sync_key_frames = export_metadata_yaml.get('time_sync_groups', [])

frames = []

# Iterate over synchronised key frames (1 x Lidar + 6 x Cameras)
for idx, sync_key_frame in enumerate(sync_key_frames):
    sample = pcd_setup.pcd_struct
    # Set LIDAR url
    lidar_asset_id = sync_key_frame['lidar']['global_id']
    sample['pcd']['url'] = upload_metadata_json['assets_ids'][
        str(lidar_asset_id)
    ]['s3_url']

    # Set frame timestamp
    total_nanosec = (
        sync_key_frame['stamp']['sec'] * 1000000000
        + sync_key_frame['stamp']['nanosec']
    )
    sample['timestamp'] = str(total_nanosec)

    # Set frame name based on index
    sample["name"] = "frame_" + str(idx)

    # Get and set ego pose based on index
    sample["ego_pose"] = ego_poses.getEgoPose(idx)

    # Get and Set images based on metadata
    sample["images"] = img_setup.getImages(
        sync_key_frame, upload_metadata_json
    )

    # Hard copy needed!
    frames.append(copy.deepcopy(sample))

# Save  JSON (DEBUG)
samples_json_file = local_data_directory / '3d_sample_frames.json'

with samples_json_file.open('w') as outfile:
    json.dump(frames, outfile, indent=4)

# Upload sequence sample
attributes = {"frames": frames}
sample = client.add_sample(dataset, seq_name, attributes)
