"""
Script: penalty_manager.py

Description:
    This module provides the RoutePenaltyManager class, a utility designed to
    dynamically adjust the traversal cost of edges in a CARLA navigation graph.
    The manager reads obstacle definitions from a YAML configuration file,
    interprets them as physical blockages or restricted areas in the world, and
    increases the weight (length) of graph edges located near those obstacles.
    This mechanism forces CARLA’s route planner to avoid obstructed or hazardous
    segments without modifying the underlying road network.

Usage:
    # 1. Initialize the manager with a navigation graph
    rpm = RoutePenaltyManager(graph)

    # 2. Load all obstacles from a YAML file
    rpm.load_obstacles("obstacles.yaml")

    # 3. Apply penalties to edges affected by nearby obstacles
    rpm.apply_penalties(penalty_value=1000.0, radius=5.0)

    # 4. Remove all penalties and restore original lengths
    rpm.remove_penalties()

Data Requirements:
    • The navigation graph must contain edges with:
        - "entry_waypoint": CARLA waypoint
        - "exit_waypoint": CARLA waypoint
        - "path": list of CARLA waypoints
        - "length": numeric cost used by the planner

    • CARLA waypoints must include:
        wp.transform.location.x
        wp.transform.location.y
        wp.transform.location.z

YAML Requirements:
    The expected YAML format includes scenarios → props → transforms:

        scenarios:
          example_scenario:
            props:
              static.prop.streetbarrier:
                - transform:
                    location: {x: 10.0, y: 25.0, z: 0.0}

    The loader extracts all such location entries as individual obstacle points.

Dependencies:
    • Python 3.x
    • NumPy
    • PyYAML
    • NetworkX (or compatible graph object)
    • CARLA Python API

"""

import yaml
import numpy as np


class RoutePenaltyManager:
    def __init__(self, graph):
        """
        Initialize the RoutePenaltyManager.

        Parameters:
            graph (networkx.DiGraph or similar):
                Navigation graph where each edge contains waypoint and length
                metadata. This graph will be dynamically modified when applying
                or removing penalties.
        """
        self.graph = graph
        self.original_lengths = {}  # Stores original edge lengths for recovery
    
    def load_obstacles(self, yaml_path):
        """
        Load obstacle definitions from a YAML file containing scenario-based
        prop information. All prop 'location' coordinates are extracted and
        flattened into a unified list of obstacle points.

        Parameters:
            yaml_path (str):
                Path to the YAML configuration file.

        Notes:
            - The YAML structure is expected to include:
                  scenarios → props → list of transforms → location
            - Each location entry contributes one obstacle point.
        """
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)

        scenarios = config.get("scenarios", {})
        obstacles = []

        # Iterate through all scenarios
        for scenario_name, scenario_data in scenarios.items():
            props = scenario_data.get("props", {})

            # Each prop contains one or more transforms
            for prop_id, transform_list in props.items():
                for element in transform_list:
                    transform = element.get("transform", {})
                    location = transform.get("location", None)

                    if location:
                        x = location.get("x")
                        y = location.get("y")
                        z = location.get("z", 0.0)

                        # Ensure valid numeric coordinates
                        if x is not None and y is not None:
                            obstacles.append({
                                "x": float(x),
                                "y": float(y),
                                "z": float(z)
                            })

        self.obstacles = obstacles
    
    def apply_penalties(self, penalty_value=1000.0, radius=5.0):
        """
        Apply length penalties to edges whose waypoints fall within a given radius
        of any loaded obstacle.

        Parameters:
            penalty_value (float):
                The cost added to affected edges.
            radius (float):
                Maximum distance at which an obstacle influences a waypoint.

        Notes:
            - Affected edges have their "length" attribute increased.
            - Original lengths are stored so penalties can be removed later.
        """
        for u, v, data in self.graph.edges(data=True):

            wp_list = (
                [data["entry_waypoint"]] +
                data["path"] +
                [data["exit_waypoint"]]
            )

            affected = False

            # Check each waypoint against every obstacle
            for obs in self.obstacles:
                ox, oy, oz = obs["x"], obs["y"], obs.get("z", 0.0)

                for wp in wp_list:
                    loc = wp.transform.location
                    dist = np.linalg.norm(
                        [loc.x - ox, loc.y - oy, loc.z - oz]
                    )

                    if dist < radius:
                        affected = True
                        break
                if affected:
                    break

            # Only modify the edge once
            if affected:
                if (u, v) not in self.original_lengths:
                    self.original_lengths[(u, v)] = data["length"]

                data["length"] = (
                    self.original_lengths[(u, v)] + penalty_value
                )
    
    def remove_penalties(self):
        """
        Restore original edge lengths that were modified by apply_penalties().
        This fully resets the graph to its pre-penalty state.
        """
        for (u, v), length in self.original_lengths.items():
            self.graph.edges[u, v]["length"] = length
        
        self.original_lengths = {}  # Clear stored values
