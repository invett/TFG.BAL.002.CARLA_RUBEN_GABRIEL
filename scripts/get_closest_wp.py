"""
Script Name: get_spectator_waypoint.py

Description:
    This script connects to a running CARLA simulator instance and retrieves 
    the closest driving waypoint to the spectator's current position in the world. 
    It displays the waypoint's location and rotation, and visually marks it in the 
    CARLA world using a debug string.

Use case:
    When working in CARLA (e.g., for simulation setup, debugging, or vehicle spawning),
    it’s often useful to identify the nearest waypoint relative to where the spectator 
    camera is currently positioned. This helps developers understand map coordinates, 
    navigation paths, and environment layout more intuitively.

How to run:
    1. Make sure the CARLA simulator is running (default port: 2000).
    2. Adjust the CARLA Python API path in the script if necessary:
         sys.path.append('/path/to/your/CARLA_x.x.x/PythonAPI/carla')
    3. Run this script with Python 3:
         python3 get_spectator_waypoint.py
    4. The script will print the spectator’s nearest waypoint information 
       and display a visual marker in the simulator.

Dependencies:
    - CARLA simulator (version 0.9.x)
    - Python 3.x
"""

import carla
import sys
import time

# Tweak this path to your CARLA installation
sys.path.append('/home/user/CARLA_0.9.16/PythonAPI/carla')

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(5.0)

# Change world/map
#client.load_world('Town03')

world = client.get_world()
spectator = world.get_spectator()
carla_map = world.get_map()

# Wait a moment in case the world is not fully loaded
time.sleep(1)

# Get spectator's transform
spec_transform = spectator.get_transform()
spec_location = spec_transform.location
spec_rotation = spec_transform.rotation

# print("=== SPECTATOR ===")
# print(f"Location -> x: {spec_location.x:.3f}, y: {spec_location.y:.3f}, z: {spec_location.z:.3f}")
# print(f"Rotation -> pitch: {spec_rotation.pitch:.3f}, yaw: {spec_rotation.yaw:.3f}, roll: {spec_rotation.roll:.3f}")

# Get the closest waypoint to the spectator
waypoint = carla_map.get_waypoint(spec_location, project_to_road=True, lane_type=carla.LaneType.Driving)

if waypoint is not None:
    wp_loc = waypoint.transform.location
    wp_rot = waypoint.transform.rotation

    print("\n=== CLOSEST WAYPOINT ===")
    print(f"Location -> x: {wp_loc.x:.3f}, y: {wp_loc.y:.3f}, z: {wp_loc.z:.3f}")
    print(f"Rotation -> pitch: {wp_rot.pitch:.3f}, yaw: {wp_rot.yaw:.3f}, roll: {wp_rot.roll:.3f}")

    # Draw a string on the waypoint
    world.debug.draw_string(
        wp_loc,
        'WAYPOINT',
        draw_shadow=False,
        color=carla.Color(r=0, g=255, b=0),
        life_time=10.0,
        persistent_lines=True
    )
else:
    print("No waypoint was found near the spectator")
