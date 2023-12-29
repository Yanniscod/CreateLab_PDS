# # Author: Addison Sears-Collins
# # Date: October 22, 2021
# # Description: Launch a two-wheeled robot using the ROS 2 Navigation Stack. 
# #              The spawning of the robot is performed by the Gazebo-ROS spawn_entity node.
# #              The robot must be in both SDF and URDF format.
# #              If you want to spawn the robot in a pose other than the default, be sure to set that inside
# #              the nav2_params_path yaml file: amcl ---> initial_pose: [x, y, z, yaw]
# #              We use preferred lanes here so the robot only travels along specific paths inside the world.
# # https://automaticaddison.com

# import os
# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
# from launch.conditions import IfCondition, UnlessCondition
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch.substitutions import Command, LaunchConfiguration, PythonExpression
# from launch_ros.actions import Node
# from launch_ros.substitutions import FindPackageShare

# def generate_launch_description():
#   package_name = 'mob_rob_loca'
#   default_launch_dir = 'launch'
#   map_file_path = 'maps/circuit.yaml'
#   nav2_params_path = 'params/nav2_essentials.yaml'
#   robot_localization_file_path = 'config/ekf.yaml'
#   rviz_config_file_path = 'rviz/filter.rviz'
#   urdf_file_path = 'urdf/edison.urdf'

#   ########## You do not need to change anything below this line ###############
  
#   # Set the path to different files and folders.  
#   pkg_share = FindPackageShare(package=package_name).find(package_name)
#   default_launch_dir = os.path.join(pkg_share, default_launch_dir)
#   default_urdf_model_path = os.path.join(pkg_share, urdf_file_path)
#   robot_localization_file_path = os.path.join(pkg_share, robot_localization_file_path) 
#   default_rviz_config_path = os.path.join(pkg_share, rviz_config_file_path)
#   nav2_dir = FindPackageShare(package='nav2_bringup').find('nav2_bringup') 
#   nav2_launch_dir = os.path.join(nav2_dir, 'launch') 
#   static_map_path = os.path.join(pkg_share, map_file_path)
#   nav2_params_path = os.path.join(pkg_share, nav2_params_path)
#   nav2_bt_path = FindPackageShare(package='nav2_bt_navigator').find('nav2_bt_navigator')
  
#   # Launch configuration variables specific to simulation
#   autostart = LaunchConfiguration('autostart')
#   headless = LaunchConfiguration('headless')
#   map_yaml_file = LaunchConfiguration('map')
#   #namespace = LaunchConfiguration('namespace')
#   params_file = LaunchConfiguration('params_file')
#   rviz_config_file = LaunchConfiguration('rviz_config_file')
#   slam = LaunchConfiguration('slam')
#   urdf_model = LaunchConfiguration('urdf_model')
#   #use_namespace = LaunchConfiguration('use_namespace')
#   use_robot_state_pub = LaunchConfiguration('use_robot_state_pub')
#   use_rviz = LaunchConfiguration('use_rviz')
#   use_sim_time = LaunchConfiguration('use_sim_time')
  
#   # Map fully qualified names to relative ones so the node's namespace can be prepended.
#   # In case of the transforms (tf), currently, there doesn't seem to be a better alternative
#   # https://github.com/ros/geometry2/issues/32
#   # https://github.com/ros/robot_state_publisher/pull/30
#   # TODO(orduno) Substitute with `PushNodeRemapping`
#   #              https://github.com/ros2/launch_ros/issues/56
#   remappings = [('/tf', 'tf'),
#                 ('/tf_static', 'tf_static')]
  
#   # Declare the launch arguments  
#   declare_namespace_cmd = DeclareLaunchArgument(
#     name='namespace',
#     default_value='',
#     description='Top-level namespace')

#   declare_use_namespace_cmd = DeclareLaunchArgument(
#     name='use_namespace',
#     default_value='false',
#     description='Whether to apply a namespace to the navigation stack')
        
#   declare_autostart_cmd = DeclareLaunchArgument(
#     name='autostart', 
#     default_value='true',
#     description='Automatically startup the nav2 stack')

#   declare_map_yaml_cmd = DeclareLaunchArgument(
#     name='map',
#     default_value=static_map_path,
#     description='Full path to map file to load')
        
#   declare_params_file_cmd = DeclareLaunchArgument(
#     name='params_file',
#     default_value=nav2_params_path,
#     description='Full path to the ROS2 parameters file to use for all launched nodes')
    
#   declare_rviz_config_file_cmd = DeclareLaunchArgument(
#     name='rviz_config_file',
#     default_value=default_rviz_config_path,
#     description='Full path to the RVIZ config file to use')

#   declare_simulator_cmd = DeclareLaunchArgument(
#     name='headless',
#     default_value='False',
#     description='Whether to execute gzclient')

#   declare_slam_cmd = DeclareLaunchArgument(
#     name='slam',
#     default_value='False',
#     description='Whether to run SLAM')

#   declare_urdf_model_path_cmd = DeclareLaunchArgument(
#     name='urdf_model', 
#     default_value=default_urdf_model_path, 
#     description='Absolute path to robot urdf file')
    
#   declare_use_robot_state_pub_cmd = DeclareLaunchArgument(
#     name='use_robot_state_pub',
#     default_value='false',
#     description='Whether to start the robot state publisher')

#   declare_use_rviz_cmd = DeclareLaunchArgument(
#     name='use_rviz',
#     default_value='false',
#     description='Whether to start RVIZ')
    
#   declare_use_sim_time_cmd = DeclareLaunchArgument(
#     name='use_sim_time',
#     default_value='false',
#     description='Use simulation (Gazebo) clock if true')

#   declare_use_simulator_cmd = DeclareLaunchArgument(
#     name='use_simulator',
#     default_value='False',
#     description='Whether to start the simulator')

#   # Specify the actions

#   # Start robot localization using an Extended Kalman filter
#   start_robot_localization_cmd = Node(
#     package='robot_localization',
#     executable='ekf_node',
#     name='ekf_filter_node',
#     output='screen',
#     parameters=[robot_localization_file_path, 
#     {'use_sim_time': use_sim_time}])

#   # Subscribe to the joint states of the robot, and publish the 3D pose of each link.
#   start_robot_state_publisher_cmd = Node(
#     condition=IfCondition(use_robot_state_pub),
#     package='robot_state_publisher',
#     executable='robot_state_publisher',
#     parameters=[{'use_sim_time': use_sim_time,
#     'robot_description': open(default_urdf_model_path, 'r').read()}],
#     remappings=remappings)

#   # Launch RViz
#   start_rviz_cmd = Node(
#     condition=IfCondition(use_rviz),
#     package='rviz2',
#     executable='rviz2',
#     name='rviz2',
#     output='screen',
#     arguments=['-d', rviz_config_file])    

#   # Launch the ROS 2 Navigation Stack
#   start_ros2_navigation_cmd = IncludeLaunchDescription(
#     PythonLaunchDescriptionSource(os.path.join(nav2_launch_dir, 'bringup_launch.py')),
#     launch_arguments = {'slam': slam,
#                         'map': map_yaml_file,
#                         'use_sim_time': use_sim_time,
#                         'params_file': params_file,
#                         'autostart': autostart}.items())
                        
#   # UNCOMMENT HERE FOR KEEPOUT DEMO
#   start_lifecycle_manager_cmd = Node(
#     package='nav2_lifecycle_manager',
#     executable='lifecycle_manager',
#     name='lifecycle_manager_costmap_filters',
#     output='screen',
#     emulate_tty=True,
#     parameters=[{'use_sim_time': use_sim_time},
#                 {'autostart': True},
#                 {'node_names': ['filter_mask_server', 'costmap_filter_info_server']}])

#   start_map_server_cmd = Node(
#     package='nav2_map_server',
#     executable='map_server',
#     name='filter_mask_server',
#     output='screen',
#     emulate_tty=True,
#     parameters=[params_file])

#   start_costmap_filter_info_server_cmd = Node(
#     package='nav2_map_server',
#     executable='costmap_filter_info_server',
#     name='costmap_filter_info_server',
#     output='screen',
#     emulate_tty=True,
#     parameters=[params_file])

#   # Create the launch description and populate
#   ld = LaunchDescription()

#   # Declare the launch options
#   #ld.add_action(declare_namespace_cmd)
#   #ld.add_action(declare_use_namespace_cmd)
#   ld.add_action(declare_autostart_cmd)
#   ld.add_action(declare_map_yaml_cmd)
#   ld.add_action(declare_params_file_cmd)
#   #ld.add_action(declare_rviz_config_file_cmd)
#   ld.add_action(declare_simulator_cmd)
#   ld.add_action(declare_slam_cmd)
#   ld.add_action(declare_urdf_model_path_cmd)
#   ld.add_action(declare_use_robot_state_pub_cmd)  
#   ld.add_action(declare_use_rviz_cmd) 
#   ld.add_action(declare_use_sim_time_cmd)
#   ld.add_action(declare_use_simulator_cmd)

#   #ld.add_action(spawn_entity_cmd)
#   #ld.add_action(start_robot_localization_cmd)
#   #ld.add_action(start_robot_state_publisher_cmd)
#   #ld.add_action(start_rviz_cmd)
#   ld.add_action(start_ros2_navigation_cmd)
#   ld.add_action(start_lifecycle_manager_cmd)
#   #ld.add_action(start_map_server_cmd)
#   ld.add_action(start_costmap_filter_info_server_cmd)  

#   return ld
