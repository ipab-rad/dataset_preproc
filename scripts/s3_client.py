import abc
import os
import sys
import boto3
import json
from botocore.config import Config
from segments import SegmentsClient

from typing import BinaryIO


class TartanAsset:

    def __init__(self, url='', uuid=''):
        self.url = url
        self.uuid = uuid


class S3Client(abc.ABC):
    """
    Abstract base class for asset uploaders.
    """

    @abc.abstractmethod
    def upload_file(self, file: BinaryIO, file_key: str) -> TartanAsset:
        """
        Upload an asset and return the access URL.
        :param file_path: Local path to the file.
        :param file_key: Destination key in S3.
        :return: URL of the uploaded asset.
        """
        pass


class SegmentS3Client(S3Client):
    """
    Uploader for SegmentsAI S3.
    """

    def __init__(self, api_key):
        self.s3_client = SegmentsClient(api_key)

    def upload_file(self, file: BinaryIO, file_key: str) -> TartanAsset:
        """
        Uploads a file to a SegmemtsAI's S3
        """
        segment_asset = self.s3_client.upload_asset(file, file_key)

        asset = TartanAsset(segment_asset.url, segment_asset.uuid)

        return asset

    def print_datasets(self):
        datasets = self.s3_client.get_datasets()
        for dataset in datasets:
            print(dataset.name, dataset.description)


class EIDFfS3Client(S3Client):
    """
    Uploader for EIDF S3
    """

    def __init__(
        self, bucket_name: str, endpoint_url: str = "https://s3.eidf.ac.uk"
    ):
        # Needed as per EIDF instructions
        config = Config(
            request_checksum_calculation="when_required",
            response_checksum_validation="when_required",
        )

        self.s3_client = boto3.resource('s3', config=config)
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url

    def upload_file(self, file: BinaryIO, file_key: str) -> TartanAsset:
        """
        Uploads a file to EIDF S3 and returns a S3 URL
        """
        response = self.s3_client.Bucket(self.bucket_name).put_object(
            Key=file_key, Body=file
        )

        if response:
            asset = TartanAsset(
                f'{self.endpoint_url}/eidf150%3A{self.bucket_name}/{file_key}',
                'super_unique_id',
            )
            return asset

        return None

    def print_object_list(self, max_prints=None):
        bucket = self.s3_client.Bucket(self.bucket_name)

        for idx, obj in enumerate(bucket.objects.all()):
            print(f'Obj {idx}: {obj.key}')
            print(
                f'\tURL: {self.endpoint_url}/eidf150%3A{self.bucket_name}/{obj.key}'
            )
            if max_prints is not None:
                if idx > max_prints:
                    break

    def set_bucket_policy(self, policy_dict):
        bucket_policy = self.s3_client.Bucket(self.bucket_name).Policy()
        bucket_policy.put(Policy=json.dumps(policy_dict))
