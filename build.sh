#!/usr/bin/env bash
# Compile the workspace. The flag activate the parsing of IMU in rslidar_sdk.
set -e
cd "$(dirname "$0")"
source /opt/ros/${ROS_DISTRO:-humble}/setup.bash
# Il driver deve pubblicare ring e timestamp per punto (serve al deskew di rko_lio).
sed -i 's/^set(POINT_TYPE XYZI)$/set(POINT_TYPE XYZIRT)/' src/rslidar_sdk/CMakeLists.txt
colcon build --symlink-install --packages-skip rko_slam \
  --cmake-args -DENABLE_IMU_DATA_PARSE=ON
