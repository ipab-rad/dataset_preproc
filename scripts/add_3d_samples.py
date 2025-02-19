#!/usr/bin/python3

import sys
import copy
import yaml
import json
from pathlib import Path

from scripts.ego_setup import EgoPoses
from scripts.img_setup import getImages
from scripts.pcd_setup import pcd_struct
from scripts.s3_client import SegmentS3Client
from scripts.utils import get_env_var, file_exists, directory_exists


class SegmentsSampleCreator:
    def __init__(self):

        # Get Segment API key from env variable
        api_key = get_env_var('SEGMENTS_API_KEY')

        # Initialise Segments.ai client
        self.client = SegmentS3Client(api_key)

        # Based on vehicle's TF tree
        self.LIDAR_HEIGHT_FROM_GROUND_M = -1.78

    def add(
        self, dataset_name: str, sequence_name: str, local_data_directory: Path
    ):

        # Verify the dataset exists
        self.client.verify_dataset(dataset_name)

        # Verify provided data directory
        directory_exists(local_data_directory)

        # Load export_metadata.yaml
        export_metadata_file = local_data_directory / 'export_metadata.yaml'
        file_exists(export_metadata_file)

        with open(export_metadata_file) as yaml_file:
            export_metadata_yaml = yaml.safe_load(yaml_file)

        # Load upload_metadata.yaml
        upload_metadata_file = local_data_directory / 'upload_metadata.json'
        file_exists(upload_metadata_file)

        with open(upload_metadata_file) as json_file:
            upload_metadata_json = json.load(json_file)

        # Search for a .tum file
        tum_files = list(local_data_directory.glob('*.tum'))
        if not tum_files:
            raise ValueError(f'Trajectory file (.tum ) not found.')

        # Initialise ego_poses based on .tum file
        ego_poses = EgoPoses(tum_files[0])

        sync_key_frames = export_metadata_yaml.get('time_sync_groups', [])

        # Verify that the number of trajectory poses matches the number of key frames
        [ok, msg] = ego_poses.validatePoseCount(len(sync_key_frames))

        if not ok:
            raise ValueError(
                f'The number of poses is not equal to the number of key frames.\n'
                f'{msg}\n'
            )

        frames = []

        print('Extacting key frames ...')
        # Iterate over synchronised key frames (1 x Lidar + 6 x Cameras)
        for idx, sync_key_frame in enumerate(sync_key_frames):
            sample = pcd_struct
            # Set LIDAR url
            lidar_asset_id = sync_key_frame['lidar']['global_id']
            sample['pcd']['url'] = upload_metadata_json['assets_ids'][
                str(lidar_asset_id)
            ]['s3_url']

            # Set frame timestamp
            total_nanosec = (
                sync_key_frame['stamp']['sec'] * (10**9)
                + sync_key_frame['stamp']['nanosec']
            )
            sample['timestamp'] = str(total_nanosec)

            # Set frame name based on index
            sample['name'] = 'frame_' + str(idx)

            # Get and set ego pose based on index
            sample['ego_pose'] = ego_poses.getEgoPose(idx)

            # Get and Set images based on metadata
            sample['images'] = getImages(sync_key_frame, upload_metadata_json)

            # Set Top lidar height from ground_level
            sample['default_z'] = self.LIDAR_HEIGHT_FROM_GROUND_M

            # Hard copy needed!
            frames.append(copy.deepcopy(sample))

        # Save  JSON (DEBUG)
        samples_json_file = local_data_directory / '3d_sample_frames.json'

        with samples_json_file.open('w') as outfile:
            json.dump(frames, outfile, indent=4)

        # Upload sequence sample
        print('Uploading sample ...')
        attributes = {'frames': frames}
        self.client.add_sample(dataset_name, sequence_name, attributes)

        print('Done \U00002714')


if __name__ == '__main__':

    # Ensure command-line argument is provided
    if len(sys.argv) < 4:
        print(
            'ERROR: Please provide the required arguments\n'
            'add_3d_sample.py <dataset_name> <sequence_name> <data_directory>',
            file=sys.stderr,
        )
        sys.exit(1)

    # Mandatory arguments
    dataset_name = sys.argv[1]
    sequence_name = sys.argv[2]
    data_directory = Path(sys.argv[3])

    sample_creator = SegmentsSampleCreator()
    sample_creator.add(dataset_name, sequence_name, data_directory)
