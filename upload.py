import sys
import os
from segments import SegmentsClient
import json

api_key = sys.argv[1]
client = SegmentsClient(api_key)

dataset = "test_av_1"
dataset_path = "/home/alex/dataset/output/sensor/camera/fsp_l/image_rect_color/compressed/sensor/camera/fsp_l/image_rect_color/compressed"

# append the text to an existing file
log_file = open( dataset+".txt", "a")

for filename in sorted(os.listdir(dataset_path)):
    filepath = os.path.join(dataset_path, filename)
    # checking if it is a file
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as f:
            asset = client.upload_asset(f, dataset+filename)
        image_url = asset.url
        print(image_url)
        log_file.write(image_url + "\n")
log_file.close()