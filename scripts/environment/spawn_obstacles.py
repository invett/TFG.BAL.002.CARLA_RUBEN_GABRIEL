import carla
import yaml
import sys

"""
Script: Spawn_obstacles.py

Description: This script connects to an active CARLA simulation and aims to load a scenario 
defined in a YAML configuration file. Each of these scenarios contains:

            - A map name to load in CARLA.
            - A description of the scenario being loaded.
            - A collection of different props or obstacles to be used in the simulation, defined as:
    
                    + blueprint type id (static.prop.trafficbarrier)
                    + list of transforms (location [x,y,z] and rotation [pitch, yaw, roll]) following 
                      the instructions in the official CARLA documentation. 

            This script also displays a console menu listing the different scenarios available that are
            defined in the YAML to run the simulation. The user enters the number of the option they want
            to run, and the script generates all the necessary props in their specified locations and their respective
            rotations.

Use case: This tool is useful when setting up CARLA simulations involving obstacles, blocked streets, cones, barriers and more
          to conduct autonomous driving tests. The YAML structure allows quick editting of scenarios without modifying Python code
          allowing testing with different configurations.
          
Simple guide: 
    1. Make sure that the CARLA simulation has started running correctly (You can move around the map as a spectator).
    2. Verify that the YAML configuration file is in the same directory. 
    3. Run using Python 3:
            'python3 spawn_obstacles.py'
    4. Choose one of the shown scenarios to load in CARLA (Enter the number of the option you want to simulate and press 'Enter').
    5. Wait a few seconds for the simulation to load. 
    
Dependencies: 
    - CARLA simulator: (0.9.x)
    - Python 3.x
    - PyYAML ('pip install pyyaml')
"""

sys.path.append('/home/user/CARLA_0.9.16/PythonAPI/carla') #Change the path to your CARLA installation directory

client = carla.Client('localhost', 2000) #Default configuration ('localhost', port=2000)
client.set_timeout(500.0) #Waiting time to connect to the CARLA server


#Load data
def load_file(filename):
    """Reads and loads YAML configuration file and returns its contents as a dictionary.

    Args:
        filename (_str_): YAML file path

    Returns:
        dictionary: Parsed YAML structure.
    """
    
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
        
    return data

#Display menu
def display_menu():
    
    """
        Prints all available scenarios to the console.
    """
    
    for num, id in options.items():
        desc = scenarios_ids[id]["description"]
        print(f"{num}. {id}: {desc} ")
    
    

def ask_option(opt):
    
    """ Ask the user to select a scenario from the menu displayed.
    
    Args:
        opt (_dictionary_): Map of listed options.

    Returns:
        (int/None): Number of option entered or Null if exiting ('Q')
    """
    
    valid = False

    while not valid:
    
        try:
            entry = input("Select one of the options to run the simulation (enter Q to exit): ").strip()
        
            if entry.lower() == "q":
                choice = None
                valid = True
            
            else:
                choice = int(entry)
            
                if choice not in opt:
                    print(f"not a valid option. Try between {min(opt)} and {(max(opt))}")  
                else:
                    valid = True
                
        except ValueError:
            print("not a valid option...")
            
    return choice
    
config = load_file('Obstacles.yaml') #Load structure with all scenarios

scenarios_ids = config["scenarios"] #Access the ‘scenarios’ section of YAML.

options = {i: name for i, name in enumerate(scenarios_ids.keys(), start=1)} # Creates menu: {1: "blocked_street01", 2: "blocked_street02", ...}

display_menu() #Display options by console

choice = ask_option(options)

if choice == None:
    
    print("ending script...")    
       
else:
    
    #Accessing the YAML file information to extract the data by sections 
    
    scenario = config["scenarios"][options[choice]]
    props = scenario["props"]
    
    world = client.load_world(scenario["map"])
    blueprint = world.get_blueprint_library()

    for type_id, instances in props.items():
        
        bp = blueprint.find(type_id) #Search for blueprint type
        
        for inst in instances:
            
            #Extract location and rotation data from the YAML according to the format specified in the official CARLA documentation.
            
            transform_data = inst["transform"]
            loc = transform_data["location"]
            rot = transform_data["rotation"]

            transform = carla.Transform(carla.Location(x = float(loc["x"]),y = float(loc["y"]),z = float(loc["z"])), 
                                    carla.Rotation(pitch= float(rot["pitch"]),yaw= float(rot["yaw"]),roll= float(rot["roll"])))
        
            actor = world.try_spawn_actor(bp, transform)
        
            #Succes verification
            if actor:
                print("Spawned: ", actor.type_id)
            else:
                print("Failed to spawn: ", type_id)
