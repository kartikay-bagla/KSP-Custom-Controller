import serial.tools.list_ports
import krpc
import time

def select_port():
    """
    Lists all serial ports and asks user to select a port
    """
    while True:
        print("Avaliable Serial Ports:")
        ports = []
        for n, (port, description, hwid) in enumerate(sorted(serial.tools.list_ports.comports())):
            print("--",n, ":     ",port, "     ", description)
            ports.append(port)
        port_index = input("Enter the number of the Port")
        try:
            if int(port_index) < len(ports): #checking if port is valid
                port = ports[int(port_index)]
            else:
                raise ValueError
        except ValueError:
            print("Failed to select port. Retry.")
        else:
            return port

def get_vessel(server):
    """
    Returns active vessel from KSP given a server when in flight mode.
    """
    vessel = None
    while True:
        try: 
            vessel = server.space_center.active_vessel
            break

        except krpc.error.RPCError as e:
            print("KSP Scene Changed!")
            time.sleep(1)
        except ConnectionAbortedError:
            print("KSP has Disconnected.")
            time.sleep(1)
    return vessel

def get_server(address = krpc.DEFAULT_ADDRESS):
    """
    Returns kRPC server object given address of kRPC server.
    """
    server = None
    while server is None:
        print("Connecting")
        try:
            server = krpc.connect(name ='Controller', address= address)
        except ConnectionRefusedError: #error raised whe failing to connect to the server.
            print("Server offline")
            time.sleep(2)
    time.sleep(1)
    return server

def get_streams(server, vessel):
    """
    Returns a lot of streams for telemetry.
    (Altitude, Apoapsis, Periapsis, Resources, G-Force, TWR)
    """
    altitude = server.add_stream(getattr, vessel.flight(), 'mean_altitude')
    apoapsis = server.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
    periapsis = server.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
    resources = server.add_stream(getattr, vessel, "resources")
    g_force = server.add_stream(getattr, vessel.flight(), "g_force")
    
    thrust = server.add_stream(getattr, vessel, "thrust")
    mass = server.add_stream(getattr, vessel, "mass")
    planet = vessel.orbit.body
    mu = planet.gravitational_parameter
    r = planet.equatorial_radius
    def twr():
        try:
            a = thrust() / ((mu * mass()) / (r + altitude())**2)
        except ZeroDivisionError:
            a = 0
        return a
    return altitude, apoapsis, periapsis, resources, g_force, twr

#main_resources = ["ElectricCharge", "MonoPropellant", "LiquidFuel", "Oxidizer"]
main_resources = ["Oxidizer", "MonoPropellant", "LiquidFuel","ElectricCharge"]

def process_resources(r):
    """
    Returns a list of values between 0-1 indicating the bar value of 
    each resource ordered according to 'main_resources'
    """

    # resource_values[resource.name] = [amount, max]
    resource_values = dict()
    for resource in r:
        if resource.name not in resource_values.keys():
            resource_values[resource.name] = [0, 0]
            resource_values[resource.name][0] = resource.amount
            resource_values[resource.name][1] = resource.max
        else:
            resource_values[resource.name][0] += resource.amount
            resource_values[resource.name][1] += resource.max

    resource_values = {key: value[0]/value[1] for key, value in resource_values.items()}
    
    l = []
    for i in main_resources:
        try:
            l.append(int(resource_values[i] * 100))
        except:
            l.append(0)

    return l
