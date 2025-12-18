"""
--------------------------------------------------------------------------
Replanning Manager
--------------------------------------------------------------------------
Description:
    This module provides the ReplanningManager class, designed to interface 
    between high-level perception events (Neural Network outputs) and the 
    CARLA navigation system. It translates semantic obstruction commands 
    into specific map topology coordinates (waypoints), allowing the path 
    planner to calculate alternative routes.

Usage:
    manager = ReplanningManager(carla_map)
    blocked_wps = manager.process_nn_event(ego_transform, nn_event)

Dependencies:
    - carla (0.9.x)
    - math
--------------------------------------------------------------------------
"""

import carla
import math

class ReplanningManager:
    """
    Manages the identification of road segments that must be avoided based on
    external perception events within the CARLA simulation environment.
    """

    def __init__(self, carla_map):
        """
        Initializes the ReplanningManager.

        Args:
            carla_map (carla.Map): The simulation map object used for topology queries.
        """
        self.map = carla_map

    def process_nn_event(self, ego_transform, nn_event):
        """
        Processes a perception event to identify specific blocked waypoints within a junction.
        
        This method utilizes the junction topology to map a relative semantic command 
        (left, right, straight) to specific entry and exit waypoints of the intersection.

        Args:
            ego_transform (carla.Transform): The current transform (location and rotation) of the ego vehicle.
            nn_event (object): A data structure containing perception details. Must include:
                               - .blocked (bool): Whether an obstacle is detected.
                               - .obstacle_relative_position (str): "left", "right", or "front"/"straight".
                               - .obstacle_distance_m (float): Distance to the obstacle.

        Returns:
            list[carla.Waypoint]: A list of waypoints representing the blocked path (entry, exit, and intermediate points).
                                  Returns an empty list if no block is detected or the junction cannot be found.
        """
        if not nn_event.blocked:
            return []

        # 1. Obtain Ego Waypoint
        ego_wp = self.map.get_waypoint(
            ego_transform.location,
            project_to_road=True,
            lane_type=carla.LaneType.Driving
        )

        direction_command = nn_event.obstacle_relative_position.lower() # "left", "right", "front"
        search_distance = nn_event.obstacle_distance_m
        
        # -----------------------------------------------------------
        # STEP 1: Locate the Target INTERSECTION
        # -----------------------------------------------------------
        # Search forward to find the location of the junction
        junction_entry_wp = self._find_next_junction_entry(ego_wp, max_search_dist=search_distance + 20.0)

        if not junction_entry_wp:
            print("⚠️ No nearby junction entry found to apply the blockage.")
            return []
        
        junction = junction_entry_wp.get_junction()
        
        # -----------------------------------------------------------
        # STEP 2: Retrieve Valid (Entry, Exit) Pairs
        # -----------------------------------------------------------
        
        # This CARLA function returns all possible paths within the junction
        junction_waypoints = junction.get_waypoints(carla.LaneType.Driving)
        
        target_waypoints = []
        
        print(f"🚦 Analyzing junction with {len(junction_waypoints)} possible connections...")

        for entry_wp, exit_wp in junction_waypoints:
            # A. FILTER BY ENTRY: 
            # We are only interested in paths starting from OUR entry point (or very close to it).
            # A tolerance of 2.5 meters is used to ensure a match.
            if entry_wp.transform.location.distance(junction_entry_wp.transform.location) > 2.5:
                continue

            # B. FILTER BY ANGLE:
            angle = self._calculate_turn_angle(entry_wp, exit_wp)
            
            # Classify if this pair corresponds to the NN command
            is_match = False
            
            if "left" in direction_command:
                # Left turn: -135 to -45 degrees
                if -135 <= angle <= -45:
                    is_match = True
            elif "right" in direction_command:
                # Right turn: 45 to 135 degrees
                if 45 <= angle <= 135:
                    is_match = True
            elif "front" in direction_command or "straight" in direction_command:
                # Straight: -45 to 45 degrees
                if -45 <= angle <= 45:
                    is_match = True

            if is_match:
                print(f"   🚫 Blocking branch: {direction_command.upper()} (Angle: {angle:.1f}°)")
                # Add entry and exit so the PenaltyManager can penalize the edge
                target_waypoints.append(entry_wp)
                target_waypoints.append(exit_wp)

        return target_waypoints

    # ---------------------------------------------------
    # Auxiliary Methods (Geometric and Map Logic)
    # ---------------------------------------------------

    def _find_next_junction_entry(self, start_wp, max_search_dist=50.0):
        """
        Navigates the road topology forward to locate the entry waypoint of the 
        immediate next junction.
        
        This method ignores the current junction if the vehicle is already inside one,
        searching strictly for the subsequent intersection.

        Args:
            start_wp (carla.Waypoint): The starting waypoint for the search.
            max_search_dist (float): The maximum distance (in meters) to search forward.

        Returns:
            carla.Waypoint: The waypoint at the entry of the next junction, or None if not found.
        """
        current_wp = start_wp
        dist_traveled = 0.0
        
        # Reduced step to 1.0m to avoid skipping road sections on very short paths
        step = 1.0 

        # 1. Identify ID of the current junction to ignore it
        initial_junction_id = None
        if start_wp.is_junction:
            initial_junction_id = start_wp.get_junction().id

        while dist_traveled < max_search_dist:
            next_wps = current_wp.next(step)
            if not next_wps:
                return None 
            
            # Take the first path (assuming single lane or main path for search)
            current_wp = next_wps[0]
            dist_traveled += step
            
            # 2. Check if it is a junction
            if current_wp.is_junction:
                found_junction = current_wp.get_junction()
                
                # 3. CRITICAL: Only return if it is a DIFFERENT junction than the current one
                if initial_junction_id is None or found_junction.id != initial_junction_id:
                    return current_wp
            
        return None

    def _calculate_turn_angle(self, entry_wp, exit_wp):
        """
        Computes the signed turn angle between the entry and exit vectors of a junction path.

        Args:
            entry_wp (carla.Waypoint): The waypoint entering the junction.
            exit_wp (carla.Waypoint): The waypoint exiting the junction.

        Returns:
            float: The angle in degrees, normalized within the range [-180, 180].
        """
        entry_vec = entry_wp.transform.get_forward_vector()
        entry_angle = math.atan2(entry_vec.y, entry_vec.x)
        
        exit_vec = exit_wp.transform.get_forward_vector()
        exit_angle = math.atan2(exit_vec.y, exit_vec.x)
        
        angle_diff = math.degrees(exit_angle - entry_angle)
        
        # Normalize
        while angle_diff > 180:
            angle_diff -= 360
        while angle_diff < -180:
            angle_diff += 360
            
        return angle_diff