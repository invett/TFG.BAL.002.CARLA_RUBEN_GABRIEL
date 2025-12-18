"""
--------------------------------------------------------------------------
Perception Event Data Structure
--------------------------------------------------------------------------
Description:
    This module defines the PerceptionEvent data class, which serves as a 
    standardized container for perception data received from external sources 
    (such as Neural Networks or sensor fusion modules). It encapsulates 
    information regarding obstacle detection, blockage status, and spatial 
    orientation relative to the ego vehicle.

Usage:
    # Direct instantiation
    event = PerceptionEvent(
        blocked=True, 
        confidence_blocked=0.95, 
        obstacle_relative_position="left", 
        obstacle_distance_m=15.0, 
        free_directions=["right", "straight"], 
        notes="Construction work detected"
    )

    # From JSON dictionary
    data_dict = {"blocked": True, "obstacle_distance_m": 12.5}
    event = PerceptionEvent.from_json(data_dict)

Dependencies:
    - dataclasses
    - typing
--------------------------------------------------------------------------
"""

from dataclasses import dataclass
from typing import List

@dataclass
class PerceptionEvent:
    """
    A data class representing a single perception event regarding road blockages.

    Attributes:
        blocked (bool): Indicates if a path is currently obstructed.
        confidence_blocked (float): The probability score (0.0 to 1.0) of the blockage detection.
        obstacle_relative_position (str): The relative direction of the obstacle (e.g., "left", "right", "front").
        obstacle_distance_m (float): The distance to the detected obstacle in meters.
        free_directions (List[str]): A list of directions that are perceived as clear/navigable.
        notes (str): Additional metadata or descriptive text regarding the event.
    """
    blocked: bool
    confidence_blocked: float
    obstacle_relative_position: str
    obstacle_distance_m: float
    free_directions: List[str]
    notes: str

    @classmethod
    def from_json(cls, data: dict) -> "PerceptionEvent":
        """
        Factory method to create a PerceptionEvent instance from a dictionary.

        This method safely parses a dictionary (e.g., from a JSON payload), providing 
        default values for missing keys to ensure the object is always valid.

        Args:
            data (dict): A dictionary containing perception data fields.

        Returns:
            PerceptionEvent: An initialized instance of the class.
        """
        return cls(
            blocked=data.get("blocked", False),
            confidence_blocked=data.get("confidence_blocked", 0.0),
            obstacle_relative_position=data.get("obstacle_relative_position", ""),
            obstacle_distance_m=data.get("obstacle_distance_m", float("inf")),
            free_directions=data.get("free_directions", []),
            notes=data.get("notes", "")
        )