#!/usr/bin/python3

import subprocess
import sys
import os
from pathlib import Path


def run_mola_lidar_odometry(rosbag_path, output_dir):
    """Run mola-lidar-odometry-cli with the given ROS bag file and output directory."""

    # Validate input file
    if not os.path.isfile(rosbag_path):
        print(
            f"Error: ROS bag file '{rosbag_path}' does not exist.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate output directory
    if not os.path.isdir(output_dir):
        print(
            f"Error: Output directory '{output_dir}' does not exist.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Extract rosbag filename without extension
    rosbag_name = Path(rosbag_path).stem

    # Define output file paths
    output_tum_path = os.path.join(output_dir, f"{rosbag_name}_trajectory.tum")
    output_map_path = os.path.join(output_dir, f"{rosbag_name}_map.simplemap")

    # Use default config file
    mola_config_path = "$(ros2 pkg prefix mola_lidar_odometry)/share/mola_lidar_odometry/pipelines/lidar3d-default.yaml"

    # Construct the command
    cmd = (
        f"mola-lidar-odometry-cli "
        f"-c {mola_config_path} "
        f"--input-rosbag2 {rosbag_path} "
        f"--lidar-sensor-label /sensor/lidar/top/points "
        f"--output-tum-path {output_tum_path} "
        f"--output-simplemap {output_map_path}"
    )

    # Run the command
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, text=True, capture_output=True
        )
        print("Output:\n", result.stdout)
        if result.stderr:
            print("Error:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Command failed with error:\n", e.stderr, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python3 get_ego_trajectory.py <path_to_rosbag.mcap> <output_directory>",
            file=sys.stderr,
        )
        sys.exit(1)

    rosbag_path = sys.argv[1]
    output_dir = sys.argv[2]

    run_mola_lidar_odometry(rosbag_path, output_dir)
