# dataset_preproc

Dataset pre-processing: consume mcap bags to produce annotation compatible data

## Segments API key

You will need your segments.ai API key to upload/create datasets. Save it as an environment variable and/or copy paste it as required

## How to use

### Build and run the Docker container interactively

`./dev.sh -l -p /PATH/TO/ROSBAGS`

### Edit & update the config/av.yaml if necessary

Example `exporter_config.yaml` file in ros2_bag_exporter pkg

### Extract data from .mcap ROSbag

`ros2 run ros2_bag_exporter bag_exporter --ros-args -p config_file:="config/av.yaml"`

### Upload data sequence to segments.ai

`python3 ./scripts/upload.py YOUR_API_KEY`

### Add uploaded assets to samples (For an existing dataset)

`python3 ./scripts/add_samples.py YOUR_API_KEY`
