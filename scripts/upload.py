#!/usr/bin/python3

import sys
import os
import json
import yaml
from pathlib import Path
from copy import deepcopy
from segments import SegmentsClient, typing

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

local_data_directory = Path(sys.argv[1])
if not local_data_directory.exists():
    print(
        f'ERROR: Provided directory \'{local_data_directory}\' does not exist.',
        file=sys.stderr,
    )
    sys.exit(1)

# Load export_metadata.yaml
metadata_file = local_data_directory / 'export_metadata.yaml'
if not metadata_file.is_file():
    print(
        f'ERROR: Metadata file \'{metadata_file}\' not found.', file=sys.stderr
    )
    sys.exit(1)

with open(metadata_file) as file:
    export_metadata_yaml = yaml.safe_load(file)

# Ensure rosbags list is valid
if (
    'rosbags' not in export_metadata_yaml
    or not export_metadata_yaml['rosbags']
):
    print(
        'ERROR: \'rosbags\' key missing or empty in metadata file.',
        file=sys.stderr,
    )
    sys.exit(1)

urls_list = {'assets_ids': {}}

# Default file metadata structure
file_dict = {
    'local_file': '',
    'label': '',
    'uuid': '',
    's3_url': '',
}


# Function to upload files
def upload_file(local_file_path: Path, label: str):
    """
    Uploads file to Segments.ai and returns asset info.

    :param: local_file_path: File to be uploaded
    :param: label: Desired label for the file

    """
    if not local_file_path.is_file():
        print(f'WARNING: File not found: {local_file_path}', file=sys.stderr)
        return None  # Return None to indicate failure

    with local_file_path.open('rb') as f:
        asset = client.upload_asset(f, label)
        return asset


def show_progress_bar(progress, total, bar_length=50):
    """
    Displays or a console progress bar.

    :param progress: Current progress (int)
    :param total: Total value corresponding to 100% (int)
    :param bar_length: Character length of the progress bar (int)
    """
    # Calculate progress as a fraction and percentage
    fraction = progress / total
    percent = int(fraction * 100)

    # Create the bar string with '=' for completed part and '-' for remaining part
    completed_length = int(round(bar_length * fraction))
    bar = '=' * completed_length + '-' * (bar_length - completed_length)

    # Print the progress bar with carriage return to overwrite the line
    sys.stdout.write(f'\r\U0001F4E4 Uploading: |{bar}| {percent} %')
    sys.stdout.flush()


# Ensure we don't easily overwrite a previous generated file
upload_metadata_file = local_data_directory / 'upload_metadata.json'
if upload_metadata_file.exists():
    print(
        'WARN: \'upload_metadata.json\' already exists. '
        'This script assumes the data has not been uploaded yet. '
        'Delete the file if you want to proceed.',
        file=sys.stderr,
    )
    sys.exit(1)

rosbag_name = Path(export_metadata_yaml['rosbags'][0]).stem
total_goups = len(export_metadata_yaml.get('time_sync_groups', []))
progress = 1

# Iterate through all time-sync groups
for sync_group in export_metadata_yaml.get('time_sync_groups', []):

    show_progress_bar(progress, total_goups)

    # Process Lidar files meta
    lidar_dict = deepcopy(file_dict)
    lidar_dict['local_file'] = sync_group['lidar']['file']

    lidar_file = Path(sync_group['lidar']['file'])
    lidar_label = f'{rosbag_name}_lidar_top_{lidar_file.name}'
    lidar_dict['label'] = lidar_label

    lidar_file_path = local_data_directory / sync_group['lidar']['file']
    lidar_asset = upload_file(lidar_file_path, lidar_label)

    if lidar_asset is not None:
        lidar_dict['uuid'] = lidar_asset.uuid
        lidar_dict['s3_url'] = lidar_asset.url
    else:
        lidar_dict['uuid'] = 'UPLOAD_FAIL'
        lidar_dict['s3_url'] = 'UPLOAD_FAIL'

    urls_list['assets_ids'][str(sync_group['lidar']['global_id'])] = lidar_dict

    # Process Camera files meta
    for cam in sync_group.get('cameras', []):

        cam_dict = deepcopy(file_dict)
        cam_dict['local_file'] = cam['file']

        cam_label = (
            f"{rosbag_name}_camera_{cam['name']}_{Path(cam['file']).name}"
        )
        cam_dict['label'] = cam_label

        cam_file_path = local_data_directory / cam['file']

        cam_asset = upload_file(cam_file_path, cam_label)
        if cam_asset is not None:
            cam_dict['uuid'] = cam_asset.uuid
            cam_dict['s3_url'] = cam_asset.url
        else:
            cam_dict['uuid'] = 'UPLOAD_FAIL'
            cam_dict['s3_url'] = 'UPLOAD_FAIL'

        urls_list['assets_ids'][str(cam["global_id"])] = cam_dict

    progress += 1

# Save metadata as JSON
with upload_metadata_file.open('w') as outfile:
    json.dump(urls_list, outfile, indent=4)

print(f'\n\n\U0001F680 Uploading metadata saved as: {upload_metadata_file}\n')
