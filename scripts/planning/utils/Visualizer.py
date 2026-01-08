"""
--------------------------------------------------------------------------
Visualizer
--------------------------------------------------------------------------
Description:
    This module provides the Visualizer class, capable of rendering 
    telemetry data and debugging information. It operates on two layers:
    1. 2D HUD: Overlays text metrics on the camera image using OpenCV.
    2. 3D World: Draws path markers directly into the CARLA simulation 
       environment for spatial debugging.

Usage:
    viz = Visualizer()
    
    # 2D Overlay
    viz.draw_hud(image, speed, target, angle, idx, total)
    
    # 3D Path
    viz.draw_route_in_world(world, route, current_index)

Dependencies:
    - carla (0.9.x)
    - cv2 (opencv-python)
--------------------------------------------------------------------------
"""

import cv2
import carla

class Visualizer:
    """
    Handles the graphical representation of vehicle state and route data.
    """

    def __init__(self):
        """
        Initializes the visualizer styles (fonts and colors).
        """
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Color definitions (B, G, R) for OpenCV or (R, G, B) depending on usage,
        # but typical OpenCV text uses tuples.
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        
    def draw_hud(self, image, speed_kmh, target_speed, angle, wp_idx, total_wp):
        """
        Renders a Heads-Up Display (HUD) overlay on the provided image buffer.

        Displays real-time metrics including speed, target speed, steering angle,
        and route progress.

        Args:
            image (numpy.ndarray): The image array (BGRA) to draw on. Modified in-place.
            speed_kmh (float): Current vehicle speed.
            target_speed (float): Desired target speed.
            angle (float): Current steering control angle.
            wp_idx (int): Index of the current target waypoint.
            total_wp (int): Total number of waypoints in the route.
        """
        lines = [
            (f'Speed: {int(speed_kmh)} km/h', (30, 30), self.white),
            (f'Target: {int(target_speed)} km/h (W+/S-)', (30, 50), self.green),
            (f'Steer: {round(angle, 1)} deg', (30, 70), self.white),
            (f'WP: {wp_idx}/{total_wp}', (30, 90), self.white)
        ]
        
        # Iterate and draw each line with a slight shadow/outline effect (thickness=1)
        for text, org, color in lines:
            cv2.putText(image, text, org, self.font, 0.5, color, 1, cv2.LINE_AA)
            
    def draw_route_in_world(self, world, route, current_index):
        """
        Draws 3D debug markers in the CARLA world to visualize the path ahead.

        It renders a 'lookahead' segment of the route using CARLA's debug helper.
        Markers change color to indicate proximity to the destination.

        Args:
            world (carla.World): The simulation world object.
            route (list): The list of (waypoint, road_option) tuples.
            current_index (int): The current index of the vehicle in the route.
        """
        # Visualization Lookahead: Draw only the next 15 points to save performance
        lookahead_range = 15
        
        for i in range(lookahead_range):
            idx = current_index + i
            
            # Boundary check
            if idx < len(route) - 1:
                # Retrieve location from the waypoint object
                loc = route[idx][0].transform.location
                
                # Dynamic Coloring Logic:
                # - Blue: Normal path
                # - Red: End of route approaching (< 25 points remaining)
                if len(route) - idx < 25:
                    color = carla.Color(255, 0, 0) # Red
                else:
                    color = carla.Color(0, 0, 255) # Blue

                # Draw the marker ('^')
                # life_time=0.1 ensures the marker disappears quickly, creating 
                # an animation effect as the car moves without cluttering the map.
                world.debug.draw_string(
                    loc, 
                    '^', 
                    draw_shadow=False, 
                    color=color, 
                    life_time=0.1, 
                    persistent_lines=True
                )