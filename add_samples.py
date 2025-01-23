import sys
from segments import SegmentsClient
import json

api_key = sys.argv[1]
client = SegmentsClient(api_key)

dataset = "GreatAlexander/Test_AV_Images"

name = "sequence_1"

image_urls = [
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/6f7bc1c9-d9b2-484e-8d71-169eee9c03d4.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/38fed651-83fc-4f14-9686-5a69379bee3d.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/60ec897a-3c85-4594-b71b-144c7317f3bf.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/25fded2f-a196-437b-a52d-f35781492da9.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/0b8c6fac-70e7-46ff-a69e-adec50d6553a.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/98955277-a128-4d54-b0b9-7c7f7f32310c.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/1b051338-fb46-4187-87b5-596fc576d8e1.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/457990e8-cbc3-41c6-97c1-41320efad7be.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/d92e5a78-47e6-4fd6-b2cf-2723e46b9672.jpg",
    "https://segmentsai-prod.s3.eu-west-2.amazonaws.com/assets/GreatAlexander/2b58d346-9c95-4bb9-a8fd-36c474fa3037.jpg",
]

frames = [
    {
        "name": "frame_00000.jpg",
        "image": {
            "url": image_urls[0],
        },
    },
    {
        "name": "frame_00001.jpg",
        "image": {
            "url": image_urls[1],
        },
    },
    {
        "name": "frame_00002.jpg",
        "image": {
            "url": image_urls[2],
        },
    },
    {
        "name": "frame_00003.jpg",
        "image": {
            "url": image_urls[3],
        },
    },
    {
        "name": "frame_00004.jpg",
        "image": {
            "url": image_urls[4],
        },
    },
    {
        "name": "frame_00005.jpg",
        "image": {
            "url": image_urls[5],
        },
    },
    {
        "name": "frame_00006.jpg",
        "image": {
            "url": image_urls[6],
        },
    },
    {
        "name": "frame_00007.jpg",
        "image": {
            "url": image_urls[7],
        },
    },
    {
        "name": "frame_00008.jpg",
        "image": {
            "url": image_urls[8],
        },
    },
    {
        "name": "frame_00009.jpg",
        "image": {
            "url": image_urls[9],
        },
    },
]

attributes = {"frames": frames}

sample = client.add_sample(dataset, name, attributes)