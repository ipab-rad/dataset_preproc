# dataset_preproc

Dataset pre-processing: consume mcap bags to produce annotation compatible data

## Usage Guide

You will need your segments.ai API key to upload/create datasets. Save it as an environment variable `SEGMENTS_API_KEY` in your host machine.

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
python3 ./scripts/generate_ego_trajectory.py <my_path_to_rosbag.mcap> <rosbag_output_dir>
```

A `.tum` file with the same name as your rosbag should appear in `<rosbag_output_dir>`.

### Upload Data Sequence to Segment.ai

To upload the extracted data sequence:

```bash
python3 ./scripts/upload.py <rosbag_output_dir>
```

After the upload, you should see an `upload_metadata.json` file inside `<rosbag_output_dir>`.

### Add a 3D Sample to Segment.ai

Create a dataset if you haven't already and extract its name.

Run the script:

```bash
python3 ./scripts/add_3d_samples.py <my_dataset_name> <sequence_name> <rosbag_output_dir>
```
Where:
- `<my_dataset_name>`: Segment.ai's dataset name
- `<sequence_name>`: Desired sequence name for the 3D sample
    - Ensure the sequence name is unique within your dataset; otherwise, this script will override it.
- `<rosbag_output_dir>`: Directory with the extracted rosbags and metadata files

If successful, you will see your new segment inside your dataset.
