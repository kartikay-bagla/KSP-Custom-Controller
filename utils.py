import serial.tools.list_ports
import krpc

def select_port():
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
            running = False #we can now end the program.
    return vessel

def get_server(address = krpc.DEFAULT_ADDRESS):
	while server is None:
        print("Connecting")
        try:
            server = krpc.connect(name ='Controller', address= address)
        except ConnectionRefusedError: #error raised whe failing to connect to the server.
            print("Server offline")
            time.sleep(2)
    time.sleep(1)
    return server
		
def process_altitude(alt):
    alt = round(alt)
    if len(str(alt)) > 6:
        print("Shit negro")
        alt = round(alt/10**6, 6-len(str(alt//10**8)))
    else:
        alt = str(alt)

    return "ALT: "+alt

def process_throttle(value):
    t = int(value.decode().strip())
    t = t/1023
    return t

def get_streams(vessel):
    # Set up streams for telemetry
    altitude = server.add_stream(getattr, vessel.flight(), 'mean_altitude')
    apoapsis = server.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
    periapsis = server.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
    resources = server.add_stream(getattr, vessel, "resources")
    
    thrust = server.add_stream(getattr, vessel, "thrust")
    mass = server.add_stream(getattr, vessel, "mass")
    planet = vessel.orbit.body
    mu = planet.gravitational_parameter
    r = planet.equatorial_radius
    def twr():
        return (thrust() / (mu * mass()) / (r + altitude()))
    return altitude, apoapsis, peapsis, resources, twr

main_resources = ["ElectricCharge", "MonoPropellant", "LiquidFuel", "Oxidizer"]

def process_resources(r):
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
    return resource_values
