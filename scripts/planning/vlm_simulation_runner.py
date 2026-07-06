"""
--------------------------------------------------------------------------
VLM Simulation Runner
--------------------------------------------------------------------------
Description:
    Main script that orchestrates the autonomous driving simulation in CARLA.
    It integrates a Visual Language Model (VLM) via the Groq API for 
    real-time semantic obstacle perception (multi-camera vision).
    Coordinates the vehicle, the telemetry graphical interface (HUD), and the 
    dynamic route replanning in case of blockages.

Usage:
    python vlm_simulation_runner.py

Dependencies:
    - carla (0.9.x)
    - opencv-python (cv2)
    - requests
    - yaml
    - agents.navigation.behavior_agent
    - navigation (custom)
--------------------------------------------------------------------------
"""

# Version without segmentation
import carla
import random
import time
import cv2
import numpy as np
import threading
import queue
import json
import base64
import requests
import os 
import math
import sys
import yaml
from collections import deque
from dataclasses import dataclass

# --- PATH TO CARLA AND NAVIGATION MODULES ---
sys.path.append('path/to/carla')
from agents.navigation.behavior_agent import BehaviorAgent
from navigation import RouteManager

# --- CONFIGURATION ---
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct" 
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
AI_WIDTH = 800
AI_HEIGHT = 600

TM_PORT = 8000 

# --- GROQ CONFIGURATION ---
GROQ_API_KEY = "API_KEY"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# --- TIME AND OBSTACLE CONFIGURATION ---
NORMAL_FPS = 20.0        
SLOW_MOTION_FACTOR = 1.0 
FIXED_DELTA_SECONDS = 1.0 / NORMAL_FPS 
FIXED_OBSTACLE_DISTANCE = 100.0  # Fixed distance for ReplanningManager

@dataclass
class PerceptionEvent:
    """
    Data structure that encapsulates the result of the perception analysis.
    """
    blocked: bool
    confidence_blocked: float
    obstacle_relative_position: str
    obstacle_distance_m: float
    free_directions: list
    notes: str
    source: str = "SYSTEM"

# Global State
current_rgb_data = None
last_event = PerceptionEvent(False, 0.0, "none", FIXED_OBSTACLE_DISTANCE, [], "Starting...") 
manual_event = None 
exit_flag = False
ai_is_busy = False 
last_ai_latency = 0.0 
ai_history = deque(maxlen=5)

# --- YAML READING FUNCTIONS ---
def load_yaml(filename):
    """
    Loads a YAML configuration file.

    Args:
        filename (str): Path to the YAML file to read.

    Returns:
        dict: Dictionary with the parsed data, or aborts execution if it doesn't exist.
    """
    try:
        with open(filename, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found.")
        sys.exit(1)

def display_menu(scenarios):
    """
    Displays the scenario selection menu to the user via terminal.

    Args:
        scenarios (dict): Dictionary of scenarios loaded from the YAML.

    Returns:
        dict: Mapping of numerical indices to scenario identifiers.
    """
    print("\n" + "="*50)
    print("🚦 SCENARIO SELECTION FOR CARLA+GROQ 🚦")
    print("="*50)
    options = {}
    for i, (scenario_id, data) in enumerate(scenarios.items(), start=1):
        options[i] = scenario_id
        desc = data.get("description", "No description").strip().split('\n')[0]
        print(f" {i}. {scenario_id} - {desc}")
    print("="*50)
    return options

def ask_option(options):
    """
    Prompts the user to select a scenario from the menu.

    Args:
        options (dict): Dictionary with the valid options.

    Returns:
        str or None: Chosen scenario ID or None if the user decides to quit.
    """
    while True:
        entry = input("\nSelect the scenario number (or 'Q' to quit): ").strip()
        if entry.lower() == 'q': return None
        try:
            choice = int(entry)
            if choice in options: return options[choice]
            else: print(f"⚠️ Invalid option. Choose a number between 1 and {max(options.keys())}.")
        except ValueError:
            print("⚠️ Invalid input. Please enter a number.")

def ask_obstacles():
    """
    Asks the user whether to spawn physical obstacles in the simulation.

    Returns:
        bool: True if the user accepts, False otherwise.
    """
    while True:
        entry = input("Do you want to spawn physical obstacles on the route? (Y/N): ").strip().lower()
        if entry in ['y', 'yes']: return True
        elif entry in ['n', 'no']: return False
        print("⚠️ Please answer with 'Y' or 'N'.")

# --- GROQ AND HUD FUNCTIONS ---
def extract_json(text):
    """
    Extracts a JSON object contained within a raw text string, useful for cleaning
    plain text responses returned by LLMs.

    Args:
        text (str): Raw text returned by the AI.

    Returns:
        dict: Parsed JSON dictionary, or None if it fails.
    """
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end != -1:
            return json.loads(text[start:end])
        return json.loads(text)
    except:
        return None
    
def get_current_wp_index(vehicle_loc, route, last_idx):
    """
    Calculates the index of the global route waypoint closest to the 
    vehicle's current location.

    Args:
        vehicle_loc (carla.Location): Current location of the car.
        route (list): List of waypoints making up the global route.
        last_idx (int): Index of the last visited waypoint (to optimize search).

    Returns:
        int: Index of the closest waypoint.
    """
    if not route:
        return 0
        
    min_dist = float('inf')
    best_idx = last_idx
    
    # We only search within the next 30 waypoints to avoid excessive calculations
    # and prevent the car from "jumping" to parallel sections of the same route.
    limit = min(len(route), last_idx + 30)
    for i in range(last_idx, limit):
        dist = vehicle_loc.distance(route[i][0].transform.location)
        if dist < min_dist:
            min_dist = dist
            best_idx = i
            
    return best_idx

def chat_groq(prompt, image_array):
    """
    Sends a request to the Groq Visual Language Model (VLM) processing a frame.
    Crops the original frame into three views (Left, Center, Right) to emulate
    a multi-camera system and encodes it in base64.

    Args:
        prompt (str): System/user instructions for the LLM.
        image_array (numpy.ndarray): RGB frame captured by the CARLA camera.

    Returns:
        str: Text response (JSON) from the API, or None if there is an error.
    """
    try:
        frame_bgr = image_array.copy()
        h, w = frame_bgr.shape[:2]

        # 1. Generate 3 crops (Left, Center, Right) with overlap
        left_crop = frame_bgr[int(h*0.2):int(h*0.8), 0:int(w*0.4)]
        center_crop = frame_bgr[int(h*0.2):int(h*0.8), int(w*0.3):int(w*0.7)]
        right_crop = frame_bgr[int(h*0.2):int(h*0.8), int(w*0.6):w]

        # Helper function to resize and encode in base64
        def encode_img(img):
            small = cv2.resize(img, (400, 400)) 
            # cv2.imencode EXPECTS a BGR image to generate a correct JPEG
            _, buffer = cv2.imencode('.jpg', small, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            return base64.b64encode(buffer).decode('utf-8')

        img_left_str = encode_img(left_crop)
        img_center_str = encode_img(center_crop)
        img_right_str = encode_img(right_crop)

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # 2. Build the Multi-Image payload
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user", 
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "text", "text": "--- IMAGE 1: LEFT VIEW (Left intersection exit) ---"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_left_str}"}},
                        {"type": "text", "text": "--- IMAGE 2: CENTER VIEW (Forward lane) ---"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_center_str}"}},
                        {"type": "text", "text": "--- IMAGE 3: RIGHT VIEW (Right intersection exit) ---"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_right_str}"}}
                    ]
                }
            ],
            "response_format": {"type": "json_object"}, 
            "temperature": 0.1,
            "max_tokens": 800
        }
        
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=8)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"⚠️ Error Groq Multi-View: {e}")
        return None

def draw_hud(display, speed, fps_target, active_event, wp_current, wp_total):
    """
    Draws a Head-Up Display (HUD) on the OpenCV window, showing vehicle telemetry,
    system metrics, and the AI model's reasoning.

    Args:
        display (numpy.ndarray): Current frame to draw on.
        speed (float): Current vehicle speed in km/h.
        fps_target (float): Target refresh rate.
        active_event (PerceptionEvent): Last active perception event (AI or manual).
        wp_current (int): Index of the current waypoint.
        wp_total (int): Total waypoints in the route.
    """
    h, w = display.shape[:2]
    overlay = display.copy()
    
    # --- EXISTING PANELS ---
    cv2.rectangle(overlay, (10, 10), (320, 240), (0, 0, 0), -1)
    cv2.rectangle(overlay, (10, h - 90), (w - 10, h - 10), (0, 0, 0), -1)
    
    # --- NEW PANEL: TOP RIGHT CORNER (AI History) ---
    box_width = 480
    box_height = 150
    cv2.rectangle(overlay, (w - box_width - 10, 10), (w - 10, 10 + box_height), (0, 0, 0), -1)
    
    # Apply transparency to all panels at once
    cv2.addWeighted(overlay, 0.6, display, 0.4, 0, display)

    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # General telemetry
    cv2.putText(display, f"--- TELEMETRY ---", (20, 35), font, 0.6, (255, 255, 255), 2)
    cv2.putText(display, f"Speed : {speed:.1f} km/h", (20, 65), font, 0.5, (0, 255, 255), 1)
    cv2.putText(display, f"Target FPS: {fps_target:.1f}", (20, 90), font, 0.5, (200, 200, 200), 1)
    
    ai_status_color = (0, 165, 255) if ai_is_busy else (0, 255, 0)
    ai_status_text = "THINKING..." if ai_is_busy else "IDLE"
    cv2.putText(display, f"VLM State: {ai_status_text}", (20, 115), font, 0.5, ai_status_color, 1)
    cv2.putText(display, f"VLM Latency: {last_ai_latency:.2f}s", (20, 140), font, 0.5, (255, 255, 255), 1)
    
    evt_color = (0, 0, 255) if active_event.blocked else (0, 255, 0)
    cv2.putText(display, f"Blocked: {active_event.blocked}", (20, 165), font, 0.5, evt_color, 1)
    cv2.putText(display, f"Source : {active_event.source}", (20, 185), font, 0.5, (255, 255, 255), 1)
    cv2.putText(display, f"Position: {active_event.obstacle_relative_position.upper()}", (20, 205), font, 0.5, (255, 255, 255), 1)

    cv2.putText(display, f"Route WP: {wp_current} / {wp_total}", (20, 225), font, 0.5, (255, 255, 255), 1)

    # Current Note (Bottom)
    cv2.putText(display, "CURRENT AI REASONING / NOTES:", (20, h - 65), font, 0.5, (0, 255, 255), 1)
    notes = active_event.notes
    max_chars = 90
    if len(notes) > max_chars:
        cv2.putText(display, notes[:max_chars] + "-", (20, h - 40), font, 0.5, (255, 255, 255), 1)
        cv2.putText(display, notes[max_chars:], (20, h - 20), font, 0.5, (255, 255, 255), 1)
    else:
        cv2.putText(display, notes, (20, h - 40), font, 0.5, (255, 255, 255), 1)

    cv2.putText(display, "MANUAL EVENT: [I]Front [J]Left [L]Right", (10, h - 100), font, 0.4, (200, 200, 200), 1)

    # --- NEW LOGIC: RENDER AI HISTORY ---
    cv2.putText(display, "AI REASONING HISTORY (LAST 5):", (w - box_width, 35), font, 0.5, (0, 255, 255), 1)
    
    # Loop through the history and print it line by line
    for idx, historical_note in enumerate(list(ai_history)):
        # Truncate to ~65 characters so it doesn't overflow the box
        trunc_note = historical_note[:65] + "..." if len(historical_note) > 65 else historical_note
        y_position = 60 + (idx * 20)
        cv2.putText(display, f"> {trunc_note}", (w - box_width, y_position), font, 0.4, (200, 200, 200), 1)

def vlm_worker():
    """
    Background worker thread that runs the VLM inference cycle.
    Takes the latest available frame, formulates the system prompt, and updates
    the global perception events based on the JSON responses.
    """
    global current_rgb_data, last_event, exit_flag, ai_is_busy, last_ai_latency
    while not exit_flag:
        if current_rgb_data is None:
            time.sleep(0.1)
            continue
        
        ai_is_busy = True 
        frame_to_analyze = current_rgb_data.copy()
        
        prompt = """
            You are an advanced autonomous driving perception system.
            You are provided with 3 images representing the LEFT, CENTER, and RIGHT views from the vehicle's wide-angle front camera.
            
            TASK:
            Analyze ALL THREE images to detect if there is any critical obstacle (vehicles, construction barriers, traffic cones, pedestrians, debris) blocking the path.
            - Look at Image 1 (LEFT) to see if the left turn/intersection exit is blocked.
            - Look at Image 2 (CENTER) to see if the forward lane is blocked.
            - Look at Image 3 (RIGHT) to see if the right turn/intersection exit is blocked.
            
            RULES:
            1. If ANY of the three views show an obstacle blocking the DRIVABLE PATH, "blocked" must be true.
            2. Set "obstacle_relative_position" based on which image the obstacle is in ("left", "front", or "right"). If none, return "none".
            3. If blocked front, "free_directions" could be ["left", "right"].

            Do NOT consider objects that are:
            - on sidewalks
            - behind fences
            - on parking lots not connected to the current lane
            - on the side of the road
            - street furniture (lampposts, signs, benches, walls)
            - objects outside the vehicle lane
            
            Return strictly in JSON format matching this structure:
            {
                "blocked": boolean, 
                "confidence_blocked": float, 
                "obstacle_relative_position": "front" or "left" or "right" or "none",
                "obstacle_distance_m": float,
                "free_directions": ["left", "right"],
                "notes": "E.g.: 'Center view clear, but Image 3 shows cones blocking the right exit.'"
            }
        """

        start_time = time.time()
        response_text = chat_groq(prompt, frame_to_analyze)
        duration = time.time() - start_time
        
        ai_is_busy = False 
        last_ai_latency = duration
        
        if response_text:
            data = extract_json(response_text)
            if data:
                ai_blocked = data.get("blocked", False)
                ai_notes = data.get("notes", "...")
                ai_pos = data.get("obstacle_relative_position", "none")
                
                # --- NEW: SAVE TO HISTORY AVOIDING CONSECUTIVE DUPLICATES ---
                if ai_notes and ai_notes != "...":
                    if not ai_history or ai_history[-1] != ai_notes:
                        ai_history.append(ai_notes)

                if manual_event is None:
                    last_event = PerceptionEvent(
                        blocked=ai_blocked,
                        confidence_blocked=float(data.get("confidence_blocked", data.get("confidence", 0.0))),
                        obstacle_relative_position=ai_pos,
                        obstacle_distance_m=FIXED_OBSTACLE_DISTANCE,
                        free_directions=data.get("free_directions", []),
                        notes=ai_notes,
                        source="VLM (MULTI-VIEW)"
                    )
        time.sleep(1.0)

# --- MAIN ---
def main():
    """
    Main execution function. 
    1. Loads the static configuration.
    2. Connects to the CARLA client and prepares the scenario.
    3. Spawns obstacles and the vehicle.
    4. Initializes sensors, controllers, and the AI thread.
    5. Maintains the synchronous tick loop for rendering, navigation, and telemetry.
    """
    global current_rgb_data, exit_flag, last_event, manual_event, ai_is_busy
    
    # 1. LOAD AND SELECT SCENARIO (YAML)
    print("Loading YAML configuration files...")
    config_obstacles = load_yaml('obstacles_eval.yaml')
    config_routes = load_yaml('start_end_wp.yaml')
    scenarios = config_obstacles.get("scenarios", {})
    
    options = display_menu(scenarios)
    selected_scenario_id = ask_option(options)
    if not selected_scenario_id:
        return
    spawn_obstacles_flag = ask_obstacles()
    scenario_data = scenarios[selected_scenario_id]
    map_name = scenario_data["map"]

    # 2. CONNECT TO CARLA
    print(f"\n🔌 Connecting to CARLA and loading map: {map_name}...")
    client = carla.Client('localhost', 2000)
    client.set_timeout(20.0)
    world = client.load_world(map_name) # Dynamically load chosen map
    m = world.get_map()

    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = FIXED_DELTA_SECONDS 
    world.apply_settings(settings)

    tm = client.get_trafficmanager(TM_PORT)
    tm.set_synchronous_mode(True) 

    vehicle = None
    cam_rgb = None
    ai_thread = None
    
    try:
        # 3. SPAWN OBSTACLES (IF USER CHOSE TO)
        if spawn_obstacles_flag:
            print(f"🚧 Spawning physical obstacles for '{selected_scenario_id}'...")
            bp_lib = world.get_blueprint_library()
            props = scenario_data.get("props", {})
            
            spawned_count = 0
            failed_count = 0
            
            for type_id, instances in props.items():
                prop_bp = bp_lib.find(type_id)
                for inst in instances:
                    loc = inst["transform"]["location"]
                    rot = inst["transform"]["rotation"]
                    
                    # We add +0.2 to the height (Z) to avoid collisions with the ground upon spawning
                    trans = carla.Transform(
                        carla.Location(x=float(loc["x"]), y=float(loc["y"]), z=float(loc["z"]) + 0.2), 
                        carla.Rotation(pitch=float(rot["pitch"]), yaw=float(rot["yaw"]), roll=float(rot["roll"]))
                    )
                    
                    actor = world.try_spawn_actor(prop_bp, trans)
                    if actor is not None:
                        spawned_count += 1
                    else:
                        failed_count += 1
                        
            print(f"📊 Obstacles Summary: {spawned_count} successfully spawned | {failed_count} failed due to collision.")
            world.tick()

        # 4. EXTRACT START/END COORDINATES
        route_data = config_routes.get(selected_scenario_id)
        if not route_data:
            print(f"❌ Error: Route coordinates not found for '{selected_scenario_id}'.")
            return
            
        sloc, srot = route_data['start']['location'], route_data['start']['rotation']
        eloc = route_data['end']['location']

        # IMPORTANT: We raise the Z slightly (+0.5) so there are no collisions when spawning
        start_transform = carla.Transform(
            carla.Location(x=float(sloc['x']), y=float(sloc['y']), z=float(sloc['z']) + 0.5),
            carla.Rotation(pitch=float(srot['pitch']), yaw=float(srot['yaw']), roll=float(srot['roll']))
        )
        dest_transform = carla.Transform(
            carla.Location(x=float(eloc['x']), y=float(eloc['y']), z=float(eloc['z']) + 0.5)
        )

        print(f"📍 Start Position: {start_transform.location}")
        print(f"📍 Destination Position: {dest_transform.location}")

        # 5. VEHICLE AND ROUTE SETUP (Dynamic)
        bp_lib = world.get_blueprint_library()
        vehicle_bp = bp_lib.filter('model3')[0]
        vehicle = world.spawn_actor(vehicle_bp, start_transform)

        route_manager = RouteManager(world)
        initial_route, destination = route_manager.generate_initial_route(start_transform, dest_transform)
        
        agent = BehaviorAgent(vehicle, behavior='aggressive')
        agent.set_global_plan(initial_route)

        # 6. SENSOR SETUP
        cam_bp = bp_lib.find('sensor.camera.rgb')
        cam_bp.set_attribute('image_size_x', str(DISPLAY_WIDTH))
        cam_bp.set_attribute('image_size_y', str(DISPLAY_HEIGHT))
        cam_bp.set_attribute('fov', '95') # 105
        cam_rgb = world.spawn_actor(cam_bp, carla.Transform(carla.Location(x=2.8, z=2.3), carla.Rotation(pitch=-5)), attach_to=vehicle)

        queue_rgb = queue.Queue()
        cam_rgb.listen(queue_rgb.put)

        ai_thread = threading.Thread(target=vlm_worker)
        ai_thread.start()

        handled_obstacle_locations = []
        
        current_wp_idx = 0 
        
        print("🚀 Simulation Started. The car is heading to the destination marked in the YAML.")

        # 7. MAIN LOOP
        while True:
            start_loop = time.time()
            target_frame_time = FIXED_DELTA_SECONDS * SLOW_MOTION_FACTOR if ai_is_busy else FIXED_DELTA_SECONDS
            world.tick()
            
            try:
                img_rgb = queue_rgb.get(timeout=2.0)
                
                array_rgb = np.frombuffer(img_rgb.raw_data, dtype=np.uint8).reshape(img_rgb.height, img_rgb.width, 4)
                frame_rgb = array_rgb[:, :, :3]
                current_rgb_data = frame_rgb.copy()
                    
                display = frame_rgb.copy()
                v = vehicle.get_velocity()
                speed_kmh = math.sqrt(v.x**2 + v.y**2 + v.z**2) * 3.6
                
                # --- Waypoints Calculation ---
                total_wps = len(route_manager.current_route)
                current_wp_idx = get_current_wp_index(vehicle.get_transform().location, route_manager.current_route, current_wp_idx)

                # Replanning Management
                active_event = manual_event if manual_event is not None else last_event
                if active_event.blocked:
                    ego_trans = vehicle.get_transform()
                    ego_loc = ego_trans.location
                    
                    # Check if we are in the same "bubble" of a previously handled junction (30 meters)
                    is_new_event = True
                    for handled_loc in handled_obstacle_locations:
                        # If the CAR is less than 30m from where it last replanned, it's the same junction
                        if ego_loc.distance(handled_loc) < 30.0: 
                            is_new_event = False
                            break
                            
                    if is_new_event:
                        print(f"\n⚡ [ALERT] Obstacle detected. Evaluating detour at this junction...")
                        replanned, new_route = route_manager.check_and_replan(ego_trans, active_event)
                        
                        if replanned:
                            print("✅ Route successfully recalculated. Ignoring this junction for the next 20 meters.")
                            agent.set_global_plan(new_route)
                            # WE SAVE THE CAR'S POSITION, not the projected obstacle's position
                            handled_obstacle_locations.append(ego_loc) 
                            current_wp_idx = 0
                        else:
                            print("⚠️ No alternative routes possible.")
                            handled_obstacle_locations.append(ego_loc)
                            
                        if manual_event is not None: 
                            manual_event = None

                # Control
                if agent.done():
                    print("🏁 Destination reached.")
                    break
                    
                control = agent.run_step()
                vehicle.apply_control(control)

                # HUD
                draw_hud(display, speed_kmh, 1.0/target_frame_time, active_event, current_wp_idx, total_wps)
                cv2.imshow("CARLA Perception HUD", display)
                
                key = cv2.waitKeyEx(1)
                if key == ord('q') or key == 27: break
                elif key == ord('i'): manual_event = PerceptionEvent(True, 1.0, "front", FIXED_OBSTACLE_DISTANCE, [], "Manual Override", "OVERRIDE")
                elif key == ord('j'): manual_event = PerceptionEvent(True, 1.0, "left", FIXED_OBSTACLE_DISTANCE, [], "Manual Override", "OVERRIDE")
                elif key == ord('l'): manual_event = PerceptionEvent(True, 1.0, "right", FIXED_OBSTACLE_DISTANCE, [], "Manual Override", "OVERRIDE")

            except queue.Empty:
                continue
            
            elapsed = time.time() - start_loop
            sleep_time = target_frame_time - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        exit_flag = True
        if ai_thread: ai_thread.join()
        settings.synchronous_mode = False
        world.apply_settings(settings)
        if vehicle: vehicle.destroy()
        if cam_rgb: cam_rgb.destroy()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()