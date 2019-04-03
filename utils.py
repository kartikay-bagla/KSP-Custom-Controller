import serial.tools.list_ports

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