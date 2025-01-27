import sys
import os
from segments import SegmentsClient
import json

# Dataset configuration: name, path to data, and log to keep track of uploads
dataset = "test_av_1"
# dataset_path = "/opt/ros_ws/output/sensor/lidar/top/points/sensor/lidar/top/points"
dataset_path = "/opt/ros_ws/output/sensor/camera/fsp_l/image_rect_color/compressed/sensor/camera/fsp_l/image_rect_color/compressed"

log_file = open("/opt/ros_ws/output/" + dataset + ".txt", "a")

file_upload_id = 0
max_file_upload = 10

# Setup segments.ai client up using your API key
api_key = sys.argv[1]
client = SegmentsClient(api_key)

# HACK: Skip 1 out of 2 images for synchronising with lidar
skip = True

# Given a dataset_path, loop through all files and attempt upload to segments.ai s3 bucket
for filename in sorted(os.listdir(dataset_path)):
    if skip is True:
        skip = False
        continue
    else:
        skip = True
    if file_upload_id >= max_file_upload:
        print("Done")
        break
    filepath = os.path.join(dataset_path, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as f:
            asset = client.upload_asset(f, dataset + filename)
            file_upload_id = file_upload_id + 1

        # Write down each uploaded asset s3 url as it is needed to create the dataset
        log_file.write(asset.url + "\n")
log_file.close()
