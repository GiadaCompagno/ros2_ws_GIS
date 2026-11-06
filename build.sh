#!/usr/bin/env bash
# Compile the workspace. The flag activate the parsing of IMU in rslidar_sdk.
set -e
cd "$(dirname "$0")"
source /opt/ros/${ROS_DISTRO:-humble}/setup.bash
colcon build --symlink-install --packages-skip rko_slam \
  --cmake-args -DENABLE_IMU_DATA_PARSE=ON
