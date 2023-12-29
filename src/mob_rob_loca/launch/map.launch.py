import os
from rclpy.node import Node
from launch import LaunchDescription
from ament_index_python import get_package_share_directory
from launch_ros.actions import Node
import tf2_ros
import rclpy
import time

def get_share_file(package_name, file_name):
    return os.path.join(get_package_share_directory(package_name), file_name)

def generate_launch_description():
    rob_loca_dir = get_package_share_directory('mob_rob_loca')
    map_path = os.path.join(rob_loca_dir, 'maps', 'circuit.yaml')
    keepout_mask_path = os.path.join(rob_loca_dir, 'maps', 'keepout_mask.yaml')
    nav2_params_path = os.path.join(rob_loca_dir, 'params/no_map_params.yaml')

    map_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'yaml_filename': map_path,
                     'frame_id': 'map'}],
    )

    lifecycle_nodes = ['filter_mask_server', 'costmap_filter_info_server']
    use_sim_time = False
    autostart = True

    start_lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager',
        output='screen',
        emulate_tty=True,  
        parameters=[{'use_sim_time': use_sim_time},
                    {'autostart': autostart},
                    {'node_names': lifecycle_nodes}])
    
    map_filter_node = Node(
    package='nav2_map_server',
    executable='map_server',
    name='filter_mask_server',
    output='screen',
    emulate_tty=True,
    parameters=[nav2_params_path],
    )

    start_costmap_filter_info_server_cmd = Node(
    package='nav2_map_server',
    executable='costmap_filter_info_server',
    name='costmap_filter_info_server',
    output='screen',
    )

    return LaunchDescription([
        # map_node,
        map_filter_node,
        start_costmap_filter_info_server_cmd,
        start_lifecycle_manager_node,
    ])
