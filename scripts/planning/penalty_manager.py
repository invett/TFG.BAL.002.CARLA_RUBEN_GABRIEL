"""
--------------------------------------------------------------------------
Route Penalty Manager
--------------------------------------------------------------------------
Description:
    This module provides the RoutePenaltyManager class, which is responsible 
    for dynamically modifying the cost (weight) of edges in the navigation 
    graph. It allows for the integration of both static obstacles (loaded 
    from YAML configuration) and dynamic runtime obstacles (detected via 
    perception) into the path planning process by increasing the traversal 
    cost of affected road segments.

Usage:
    penalty_manager = RoutePenaltyManager(navigation_graph)
    
    # Static Usage
    penalty_manager.load_obstacles("scenarios/obstacles.yaml")
    penalty_manager.apply_static_penalties()

    # Dynamic Usage (e.g., after perception event)
    penalty_manager.apply_penalty_near_waypoints(blocked_waypoints, penalty_value=500.0)

    # Cleanup (restore original map weights)
    penalty_manager.remove_penalties()

Dependencies:
    - yaml
    - numpy
    - networkx (implied by graph structure)
    - carla (implied by waypoint objects)
--------------------------------------------------------------------------
"""

import yaml
import numpy as np


class RoutePenaltyManager:
    """
    Applies spatial penalties to edges of a navigation graph based on proximity
    to obstacle locations. 
    
    This class supports maintaining a history of original edge weights, allowing 
    temporary penalties (e.g., for transient obstacles) to be rolled back without 
    rebuilding the entire graph.
    """

    def __init__(self, graph):
        """
        Initializes the RoutePenaltyManager.

        Args:
            graph (networkx.DiGraph): The navigation graph where edges contain 
                                      'entry_waypoint', 'exit_waypoint', and 'path' attributes,
                                      along with a 'length' attribute representing cost.
        """
        self.graph = graph
        self.original_lengths = {}
        self.static_obstacles = []

    # --------------------------------------------------
    # Static Obstacles Management (YAML)
    # --------------------------------------------------
    def load_obstacles(self, yaml_path):
        """
        Parses a YAML configuration file to extract static obstacle locations.

        This method expects a specific structure (ScenarioRunner compatible) where 
        obstacles are defined under a 'scenarios' -> 'props' hierarchy.

        Args:
            yaml_path (str): The file path to the YAML configuration.
        """
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)

        scenarios = config.get("scenarios", {})
        obstacles = []

        for scenario in scenarios.values():
            props = scenario.get("props", {})
            for transforms in props.values():
                for element in transforms:
                    location = element.get("transform", {}).get("location", {})
                    if "x" in location and "y" in location:
                        obstacles.append(
                            (float(location["x"]),
                             float(location["y"]),
                             float(location.get("z", 0.0)))
                        )

        self.static_obstacles = obstacles

    def apply_static_penalties(self, penalty_value=1000.0, radius=5.0):
        """
        Applies penalties to graph edges for all currently loaded static obstacles.

        Args:
            penalty_value (float): The cost to add to affected edges.
            radius (float): The radius in meters around the obstacle within which edges are penalized.
        """
        for obs in self.static_obstacles:
            self.apply_spatial_penalty(obs, radius, penalty_value)

    # --------------------------------------------------
    # Dynamic / Generic Penalty Application
    # --------------------------------------------------
    def apply_spatial_penalty(self, center, radius, penalty_value):
        """
        Applies a penalty to all graph edges that contain waypoints within a specified 
        radius of a spatial center point.

        This method iterates through all edges in the graph, checks the geometric 
        distance of their waypoints to the center, and increases the edge 'length' 
        (cost) if a collision is detected.

        Args:
            center (tuple): A tuple (x, y, z) representing the world coordinates of the obstacle center.
            radius (float): The influence radius in meters. Any edge passing through this sphere is penalized.
            penalty_value (float): The additive cost value.
        """
        cx, cy, cz = center

        for u, v, data in self.graph.edges(data=True):
            # Construct a full list of points defining the edge geometry
            wp_list = (
                [data["entry_waypoint"]] +
                data.get("path", []) +
                [data["exit_waypoint"]]
            )

            for wp in wp_list:
                loc = wp.transform.location
                dist = np.linalg.norm(
                    [loc.x - cx, loc.y - cy, loc.z - cz]
                )

                if dist < radius:
                    # Cache the original length if this is the first time we modify this edge
                    if (u, v) not in self.original_lengths:
                        self.original_lengths[(u, v)] = data["length"]

                    data["length"] = (
                        self.original_lengths[(u, v)] + penalty_value
                    )
                    break

    def apply_penalty_near_waypoints(self, target_waypoints, penalty_value=1000.0, radius=3.0):
        """
        Applies penalties to graph edges whose waypoints are geometrically close to 
        any of the provided target waypoints.

        This is typically used for dynamic replanning when an external manager identifies
        specific road segments (as a list of waypoints) that should be avoided.

        Args:
            target_waypoints (list[carla.Waypoint]): A list of waypoints marking the blocked area.
            penalty_value (float): The cost to add to affected edges.
            radius (float): The proximity threshold in meters.
        """
        for u, v, data in self.graph.edges(data=True):
            wp_list = (
                [data["entry_waypoint"]] +
                data["path"] +
                [data["exit_waypoint"]]
            )

            affected = False

            # Check if any point on the edge is close to any target waypoint
            for target_wp in target_waypoints:
                tloc = target_wp.transform.location

                for wp in wp_list:
                    loc = wp.transform.location
                    dist = np.linalg.norm([
                        loc.x - tloc.x,
                        loc.y - tloc.y,
                        loc.z - tloc.z
                    ])
                    if dist < radius:
                        affected = True
                        break

                if affected:
                    break

            if affected:
                if (u, v) not in self.original_lengths:
                    self.original_lengths[(u, v)] = data["length"]

                data["length"] = (
                    self.original_lengths[(u, v)] + penalty_value
                )

    # --------------------------------------------------
    # Cleanup and Restoration
    # --------------------------------------------------
    def remove_penalties(self):
        """
        Restores the original weights of all modified edges and clears the modification history.
        
        This should be called before a new planning cycle if the dynamic obstacles 
        are expected to have moved or disappeared.
        """
        for (u, v), length in self.original_lengths.items():
            self.graph.edges[u, v]["length"] = length
        self.original_lengths.clear()