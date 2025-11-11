import carla
import sys
import math
sys.path.append('/home/ruben/CARLA_0.9.16/PythonAPI/carla') # tweak to where you put carla
from agents.navigation.global_route_planner import GlobalRoutePlanner

client = carla.Client('localhost', 2000)

#client.load_world('Town03')
#time.sleep(10)

world = client.get_world()
print(client.get_world().get_spectator().get_location())

# TP to Location
# spectator = world.get_spectator()
# loc = carla.Location(0.8, 0.7, 0.0)
# rot = carla.Rotation(pitch=-90, yaw=0.0, roll=0.0)
# spectator.set_transform(carla.Transform(loc, rot))

def gen_route(inicio, fin):

    sampling_resolution = 2
    grp = GlobalRoutePlanner(world.get_map(), sampling_resolution)

    route = grp.trace_route(inicio.location, fin.location)

    for waypoint in route:
        
        world.debug.draw_string(waypoint[0].transform.location, 'X', draw_shadow=False,
            color=carla.Color(r=0, g=255, b=0), life_time=10.0,
            persistent_lines=True)
    return route

def compute_route_length(route):
    """
    route: list returned by GlobalRoutePlanner.trace_route()
    """
    length = 0.0
    for i in range(1, len(route)):
        wp_prev = route[i - 1][0].transform.location
        wp_next = route[i][0].transform.location

        dist = math.sqrt(
            (wp_next.x - wp_prev.x)**2 +
            (wp_next.y - wp_prev.y)**2 +
            (wp_next.z - wp_prev.z)**2
        )
        length += dist

    return length



spawn_point = carla.Transform(
    carla.Location(x=-9.332191, y=142.655930, z=0.2),
    carla.Rotation(0.0, 90.0, 0.0)
)

end = carla.Transform(
    carla.Location(x=-15.307164, y=168.030716, z=0.2),
    carla.Rotation(0.0, 0.0, 0.0)
)

route = gen_route(spawn_point, end)
length = compute_route_length(route)
print(f"Longitud de la ruta: {length:.2f} metros")

