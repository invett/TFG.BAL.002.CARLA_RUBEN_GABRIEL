import carla
import yaml
import tkinter 
import sys
from tkinter import  messagebox


"""
Script: Spawn_obstacles_GUI.py

Description: This script connects to an active CARLA simulation and aims to load a scenario 
defined in a YAML configuration file, similar to the 'spawn_obstacles.py' script, but now with graphic user interface. Each of these scenarios contains:

            - A map name to load in CARLA.
            - A description of the scenario being loaded.
            - A collection of different props (including route reference props marked with a comment "#Route reference") or obstacles to be used in the simulation, defined as:
    
                    + blueprint type id (static.prop.trafficbarrier)
                    + list of transforms (location [x,y,z] and rotation [pitch, yaw, roll]) following 
                      the instructions in the official CARLA documentation. 

            This script displays a graphical interface divided into two sections. 
            The upper section contains all the options available in the YAML configuration file, 
            and the lower section displays the description of the environment selected 
            by the user before starting the simulation (by pressing the run simulation button).
            In addition, when running the simulation with some of the options shown, the script will also display 
            a series of props that serve as an indication of a predetermined route for each scenario and will also 
            display text above the object indicating the start and end of the route. 

Use case: This tool is useful when setting up CARLA simulations involving obstacles, blocked streets, cones, barriers and more
          to conduct autonomous driving tests. The YAML structure allows quick editting of scenarios without modifying Python code
          allowing testing with different configurations.
          
Simple guide: 
    1. Make sure that the CARLA simulation has started running correctly (You can move around the map as a spectator).
    2. Verify that the YAML configuration file is in the same directory. 
    3. Run using Python 3:
            'python3 spawn_obstacles_GUI.py'
    4. Choose one of the shown scenarios to load in CARLA (Select the option you want by clicking on it. The description of the option will be displayed before execution).
    5. Wait a few seconds for the simulation to load. 
    6. If you want to choose other map, can repeat steps 4 and 5, or you can close the tab if you are not going to run any other simulations.
    
Dependencies: 
    - CARLA simulator: (0.9.x)
    - Tkinter (included in the standard Python library)
    - Python 3.x
    - PyYAML ('pip install pyyaml')
"""
sys.path.append('/home/user/CARLA_0.9.16/PythonAPI/carla') #Change the path to your CARLA installation directory

client = carla.Client('localhost', 2000) #Default configuration ('localhost', port=2000)
client.set_timeout(500.0) #Waiting time to connect to the CARLA server

#------ LOAD CONFIG-------------
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

#Callback when the user selects an option from the interface list
def selection(event):
    """
    Callback when the user selects an option from the interface list.
    Detects the scenario and updates the text with the description of the selected option. 

    """
    
    selected = listbox.curselection()
    
    if not selected:
        return

    scenario_key = names[selected[0]]
    descrip = scenarios_ids[scenario_key]["description"]
    desc_text.delete("1.0", tkinter.END)
    desc_text.insert(tkinter.END, descrip)

# Main simulation execution
def run_simulation():
    
    """
        Generates the graphical user interface (GUI) for selecting simulation environments. 
        The graphical interface is divided into an upper section consisting of the available options 
        and a lower section showing the description of the selected scenario.
    """
    
    choice = listbox.curselection()
    if not choice:
        messagebox.showwarning("Warning", "You must choose a scenario to continue.")
        return #Returns None

    scenario_key = names[choice[0]]
    scenario = scenarios_ids[scenario_key]
    
    world = client.load_world(scenario["map"])
    blueprint = world.get_blueprint_library()
    
    
    props = scenario["props"]
    
    start = False
    end = False
    
    for type_id, instances in props.items():
        bp = blueprint.find(type_id)
        
        
        for inst in instances:
            transform = inst["transform"]
            loc = transform["location"]
            rot = transform["rotation"]
            
            carla_transform = carla.Transform(carla.Location(x = float(loc["x"]),y = float(loc["y"]),z = float(loc["z"])), 
                                    carla.Rotation(pitch= float(rot["pitch"]),yaw= float(rot["yaw"]),roll= float(rot["roll"])))
            
            
            actor = world.try_spawn_actor(bp, carla_transform)
            world.tick() #Update world (This assure that locations for START and END reference texts are correctly updated)
            
            if actor:
                print("Spawned: ", actor.type_id)
            else:
                print("Failed to spawn: ", type_id)
                
                messagebox.showinfo("Ready...", f"Scenario {scenario_key} loaded.")
                
            #show route reference text
            z = float(loc["z"])
            rot_guide = float(rot["pitch"])
            actor_loc = actor.get_transform().location
            actor_loc.z += 2.0
            
            if actor.type_id == "static.prop.trafficcone02" and z > 6.0 and abs(rot_guide) > 50 and not start:
                
                world.debug.draw_string(
                    actor_loc,
                    "START",
                    color = carla.Color(0,0,255),
                    life_time=120.0,
                    persistent_lines=True                
                )
                start = True
            
            if actor.type_id == "static.prop.stop" and z > 6.0 and not end:
                
                world.debug.draw_string(
                    actor_loc,
                    "END",
                    color = carla.Color(0,0,255),
                    life_time=120.0,
                    persistent_lines=True                
                )
                end = True
    
config = load_file('obstacles.yaml')
scenarios_ids = config["scenarios"]
names = list(scenarios_ids.keys())
#options = {i: name for i, name in enumerate(scenarios_ids.keys(), start=1)}

#------------- GUI SETUP -----------------------
root = tkinter.Tk()
root.title("Simulation of scenarios with roadblocks")
root.geometry("500x350") #Tab size

#Scenario list
label_list = tkinter.Label(root, text="Select one of the following scenarios", font=("Arial",12))
label_list.pack(pady=5)

listbox = tkinter.Listbox(root, height=6)
listbox.pack(fill="both", expand=False, padx=20)

for name in names:
    listbox.insert(tkinter.END, name)
    
#Description box for each scenario
desc_label = tkinter.Label(root, text="Description", font=("Arial", 12))
desc_label.pack(pady=5)

desc_text = tkinter.Text(root, height=6, width=60, wrap="word")
desc_text.pack(padx=20, pady=5)

listbox.bind("<<ListboxSelect>>", selection)

# Run simulation button
run_button = tkinter.Button(root, text="Run simulation", command=run_simulation, font=("Arial", 12))
run_button.pack(pady=5)


root.mainloop()