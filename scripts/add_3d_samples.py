import sys
import copy
from segments import SegmentsClient
import json

dataset = "GreatAlexander/Test_3D_1"
name = "sequence_1"

pcd_urls = [
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/cbf35f19-5871-40ab-9fb1-6458bef82234.pcd",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/67af3d54-b25f-462d-a693-ef085e9b42ba.pcd",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/be72ffb7-8d11-44bc-a0bf-696b81c8d0df.pcd",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/1e6407d7-66ba-4f21-995b-6c9bf5cbb096.pcd",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/26e5f352-d95a-478d-92e4-8dbaecc43611.pcd",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/ac96e5b2-fe3d-4899-8129-a325e81fd728.pcd",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/28f99bba-a054-4f34-9ad2-dcda5f7d5baf.pcd",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/5d0ad3ca-aed8-438b-b2b4-702783a610c5.pcd",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/72722d9e-9e87-4442-bacd-378a274608fd.pcd",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/7022b78f-b038-4c54-8143-92813e0f807b.pcd",
]

image_urls = [
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/6e4af542-3a13-40e1-9d53-daaf34fc44aa.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/f27980dd-2484-4bee-95ca-115d34da4da4.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/d3432d95-e625-4e4c-b871-014c10414c56.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/737524c7-2a57-4278-93e0-0d8770afa85d.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/48cc7168-db72-4ed3-8248-0a553ae1f1c1.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/7be743fe-cc60-4a98-8a4d-9dd60776726c.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/92e53442-913e-469b-b2f8-f4cb4d22c9af.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/b448c722-d345-4b0e-a734-ebb17dbd93e6.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/af40047e-5fdd-46d2-a35e-5685f3416e5b.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/f2bcdf3f-ec15-4b9e-8de6-fbca59965e7c.jpg",
]

# Top lidar msg timestamps, all data is relative to the top lidar
timestamps = [
    "1731680320128386304",
    "1731680320228357120",
    "1731680320328339968",
    "1731680320428329216",
    "1731680320528308480",
    "1731680320628301824",
    "1731680320728293632",
    "1731680320828286976",
    "1731680320928278784",
    "1731680321028372992",
]

# Hard-coded ego-positions for testing purposes. Later they will come from EKF
# 8.4m/s at 100ms dt
ego_x = [
    "0.0",
    "0.84",
    "1.68",
    "2.52",
    "3.36",
    "4.2",
    "5.04",
    "5.88",
    "6.72",
    "7.56",
]

# Pointcloud dictionary structure
pcd_struct = {
    "pcd": {
        "url": pcd_urls[0],
        "type": "pcd",
    },
    "images": [],
    "ego_pose": {
        "position": {
            "x": ego_x[0],
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
    "name": names[0],
    "timestamp": timestamps[0],
}

# Front camera dictionary structure
fsp_l_struct = {
    "url": image_urls[0],
    "row": 1,  # Row when displaying multiple camera images
    "col": 1,  # Col when displaying multiple camera images
    "intrinsics": {
        "intrinsic_matrix": [
            [1451.49531, 0.0, 1218.93228],
            [0.0, 1450.7118, 683.50771],
            [0.0, 0.0, 1.0],
        ]
    },
    "extrinsics": {
        "translation": {"x": 0.543, "y": 0.300, "z": -0.290},
        "rotation": {"qx": -0.525, "qy": 0.526, "qz": -0.473, "qw": 0.473},
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

frames = []

# Build one "pcd" (pointcloud sample) at a time using structs and modifying them
# Note: A *lot* of this could/should be done with list/dictionary comprehension
for f in range(0, 10):
    pcd = pcd_struct
    pcd["pcd"]["url"] = pcd_urls[f]
    pcd["ego_pose"]["position"]["x"] = ego_x[f]
    pcd["name"] = "frame_" + str(f)
    pcd["timestamp"] = timestamps[f]
    pcd["images"] = [fsp_l_struct]
    pcd["images"][0]["url"] = image_urls[f]
    frames.append(copy.deepcopy(pcd))

attributes = {"frames": frames}

# Setup segments.ai client up using your API key
api_key = sys.argv[1]
client = SegmentsClient(api_key)
sample = client.add_sample(dataset, name, attributes)
