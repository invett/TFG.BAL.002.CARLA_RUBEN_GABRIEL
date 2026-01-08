"""
--------------------------------------------------------------------------
Camera Manager
--------------------------------------------------------------------------
Description:
    This module provides the CameraManager class, a wrapper around the 
    CARLA RGB Camera sensor. It handles the spawning of the sensor, 
    the asynchronous data retrieval, and the conversion of raw CARLA 
    buffer data into a writable NumPy array compatible with OpenCV.

Usage:
    camera_manager = CameraManager(world, ego_vehicle)
    
    # In the main loop:
    image = camera_manager.get_image()
    cv2.imshow("Camera", image)

Dependencies:
    - carla (0.9.x)
    - numpy
    - cv2 (opencv-python)
--------------------------------------------------------------------------
"""

import carla
import numpy as np
import cv2

class CameraManager:
    """
    Manages the lifecycle and data streaming of an RGB camera attached to a vehicle.
    """

    def __init__(self, world, vehicle, width=640, height=360):
        """
        Initializes the camera sensor and attaches it to the ego vehicle.

        Args:
            world (carla.World): The simulation world.
            vehicle (carla.Actor): The vehicle to which the camera will be attached.
            width (int): Horizontal resolution in pixels.
            height (int): Vertical resolution in pixels.
        """
        # 1. Configure the Blueprint
        self.blueprint = world.get_blueprint_library().find('sensor.camera.rgb')
        self.blueprint.set_attribute('image_size_x', str(width))
        self.blueprint.set_attribute('image_size_y', str(height))
        self.blueprint.set_attribute('fov', '110') # Standard FOV, adaptable if needed
        
        # 2. Define mounting position (Relative Transform)
        # Location(x=-5, z=3) places the camera behind and above the car (Third-person view)
        self.transform = carla.Transform(carla.Location(z=3, x=-5))
        
        # 3. Spawn the actor
        self.sensor = world.spawn_actor(self.blueprint, self.transform, attach_to=vehicle)
        
        # 4. Initialize buffer
        # We create a placeholder to avoid errors if called before the first frame arrives
        self.image = np.zeros((height, width, 4), dtype=np.uint8)
        
        # 5. Register Callback
        # We use a lambda to pass the data processing to our internal method
        self.sensor.listen(lambda data: self._callback(data))

    def _callback(self, data):
        """
        Processes the raw data stream from the simulation.

        Converts the CARLA RawData buffer into a structured NumPy array.
        CRITICAL: Performs a deep copy to ensure memory ownership and writability.

        Args:
            data (carla.Image): The raw image packet from the server.
        """
        # Convert raw buffer to numpy array (this is a read-only pointer to C++ memory)
        array = np.frombuffer(data.raw_data, dtype=np.dtype("uint8"))
        
        # Reshape to (Height, Width, 4 Channels - BGRA)
        array = np.reshape(array, (data.height, data.width, 4))
        
        # -----------------------------------------------------------
        # MEMORY MANAGEMENT FIX
        # -----------------------------------------------------------
        # CARLA's raw buffer is read-only. We perform a deep copy to:
        # 1. Decouple the array from the underlying C++ buffer.
        # 2. Allow OpenCV or other libraries to modify the image (draw, resize, etc.).
        # 3. Prevent 'buffer is not writable' errors.
        self.image = array.copy() 

    def get_image(self):
        """
        Retrieves the latest captured frame.

        Returns:
            numpy.ndarray: The image array in BGRA format (OpenCV compatible).
        """
        return self.image

    def destroy(self):
        """
        Cleans up the sensor actor to prevent simulation artifacts or crashes.
        """
        if self.sensor:
            self.sensor.stop()
            self.sensor.destroy()
            self.sensor = None