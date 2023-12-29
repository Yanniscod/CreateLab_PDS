import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
   rob_loca_dir = get_package_share_directory('mob_rob_loca')
   map_path = os.path.join(rob_loca_dir, 'maps', 'circuit.yaml')
   nav2_params_path = os.path.join(rob_loca_dir, 'params/edi_params_rotate_acc.yaml')

   sensor_conv_launch = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('mob_rob_loca'), 'launch'),
         '/sensor.launch.py'])
      )
   rviz_launch = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('mob_rob_loca'), 'launch'),
         '/rviz.launch.py'])
      )
   ekf_launch = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('mob_rob_loca'), 'launch'),
         '/ekf.launch.py'])
      )
   filter_launch = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('mob_rob_loca'), 'launch'),
         '/trial.launch.py'])
      )
   
   nav2_launch = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('nav2_bringup'), 'launch'),
         '/navigation_launch.py']),
         launch_arguments= {
                        'map': map_path,
                        'use_sim_time': 'false',
                        'params_file': nav2_params_path,
                        'autostart': 'true',
                        }.items()
      )
   
   plot_launch = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('mob_rob_loca'), 'launch'),
         '/plot.launch.py'])
      )

   return LaunchDescription([
      sensor_conv_launch,
      ekf_launch,
      rviz_launch,
      filter_launch,
      nav2_launch,
      # plot_launch
   ])
