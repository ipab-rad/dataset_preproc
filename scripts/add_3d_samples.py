#!/usr/bin/python3

import sys
import copy
from segments import SegmentsClient
import json

import ego_setup, img_setup, pcd_setup

dataset = "GreatAlexander/Test_3D_1"
seq_name = "sequence_6"

frames = []

# Build one "sample" (3D pointcloud + image sample) at a time using structs and modifying them
# Note: A *lot* of this could/should be done with list/dictionary comprehension
key_frames_n = len(pcd_setup.pcd_urls)
for f in range(0, key_frames_n):
    sample = pcd_setup.getSamplePCD(f)
    sample["ego_pose"] = ego_setup.getEgoPose(f)
    sample["name"] = "frame_" + str(f)
    sample["timestamp"] = pcd_setup.getTimestamp(f)
    sample["images"] = img_setup.getImages(f)
    frames.append(copy.deepcopy(sample))

attributes = {"frames": frames}

# Setup segments.ai client up using your API key
api_key = sys.argv[1]
client = SegmentsClient(api_key)
sample = client.add_sample(dataset, seq_name, attributes)
