# dataset_preproc

Dataset pre-processing: Processes MCAP bag files to generate data compatible with the [SegmentsAI](https://segments.ai/) annotation tool.

## Usage Guide

To upload and add sample data to SegmentsAI, you will need access key tokens.

### Setting Up Access Keys

Create a file named `dataset_keys.env` inside a `keys` directory in the parent directory of this repository:

```bash
mkdir -p keys && touch keys/dataset_keys.env
```

Add the following environment variables to `dataset_keys.env`:

```bash
AWS_ACCESS_KEY_ID=my_access_key_id
AWS_SECRET_ACCESS_KEY=my_secret_access_key
AWS_ENDPOINT_URL=https://s3.eidf.ac.uk
BUCKET_NAME=my_bucket_name

# SegmentsAI key
SEGMENTS_API_KEY=my_segment_ai_api_key
```

#### Important Notes
- File and path names are case-sensitive.
- The `dev.sh` script will attempt to locate the `dataset_keys.env` file. If the file is missing or incorrectly named, the script will throw an error.

For access credentials, please contact [Hector Cruz](@hect95) or [Alejandro Bordallo](@GreatAlexander).



### Build and Run the Docker Container Interactively

To build and run the Docker container interactively, use:

```bash
./dev.sh -l -p /PATH/TO/ROSBAGS
```

### Extract Data from `.mcap` ROSbag

1. Edit `config/av.yaml` to define `bag_path` and `output_dir`.
2. For further reference, check [exporter_config.yaml](https://github.com/ipab-rad/ros2_bag_exporter/blob/main/config/exporter_config.yaml).
3. Run the following command to extract data:

```bash
ros2 run ros2_bag_exporter bag_exporter --ros-args -p config_file:="config/av.yaml"
```

The extractor will create a directory named after the provided rosbag inside the `output_dir` directory. This directory will contain:
- Extracted point clouds (`.pcd`)
- Images (`.jpg`)
- `export_metadata.yaml`

We will refer to this directory as `<rosbag_output_dir>`.

### Extract Ego Trajectory from the ROSbag

To extract the ego trajectory:

```bash
python3 -m scripts.generate_ego_trajectory.py <my_path_to_rosbag.mcap> <rosbag_output_dir>
```

A `.tum` file with the same name as your rosbag should appear in `<rosbag_output_dir>`.

### Upload Data to S3

To upload the extracted data to either EIDF or SegmentsAI AWS S3, run:

```bash
python3 -m scripts.upload <rosbag_output_dir> eidf
# Or
python3 -m scripts.upload <rosbag_output_dir> segments
```

If no S3 organisation is specified, `eidf` is used by default.

After the upload, you should see an `upload_metadata.json` file inside `<rosbag_output_dir>`.

### Add a 3D Sample to Segment.ai

Create a dataset if you haven't already and extract its name.

Run the script:

```bash
python3 -m scripts.add_3d_samples.py <my_dataset_name> <sequence_name> <rosbag_output_dir>
```
Where:
- `<my_dataset_name>`: Segment.ai's dataset name
- `<sequence_name>`: Desired sequence name for the 3D sample
    - Ensure the sequence name is unique within your dataset; otherwise, the sample will not be uploaded
- `<rosbag_output_dir>`: Directory with the extracted rosbags and metadata files

If successful, you will see your new segment inside your dataset.
