import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory('gis_bringup')
    default_cfg = os.path.join(share, 'config', 'rslidar_airy.yaml')

    # Posa del lidar rispetto al robot (base_link -> rslidar).
    # DA IMPOSTARE con i valori reali di montaggio; per ora identita'.
    tf_args = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']

    declared = [DeclareLaunchArgument('config_path', default_value=default_cfg)]
    declared += [DeclareLaunchArgument(a, default_value='0.0') for a in tf_args]

    driver = Node(
        package='rslidar_sdk',
        executable='rslidar_sdk_node',
        output='screen',
        parameters=[{'config_path': LaunchConfiguration('config_path')}],
    )

    lidar_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '--x', LaunchConfiguration('x'),
            '--y', LaunchConfiguration('y'),
            '--z', LaunchConfiguration('z'),
            '--roll', LaunchConfiguration('roll'),
            '--pitch', LaunchConfiguration('pitch'),
            '--yaw', LaunchConfiguration('yaw'),
            '--frame-id', 'base_link',
            '--child-frame-id', 'rslidar',
        ],
    )

    return LaunchDescription(declared + [driver, lidar_tf])