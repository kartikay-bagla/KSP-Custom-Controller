import krpc
import time
import numpy as np
from utils import process_resources, get_vessel, get_server, get_streams

running = True
server = None

server = get_server()

print("Started")

vessel = get_vessel(server)

altitude, apoapsis, peapsis, resources, twr = get_streams(vessel)


# Pre-launch setup
# vessel.control.sas = False
# vessel.control.rcs = False
# vessel.control.throttle = 1.0
main_resources = ["ElectricCharge", "MonoPropellant", "LiquidFuel", "Oxidizer"]

#print(resource_values)
print("Main loop")
count = 0
while running:
    try:
        print("ALT: " + str(altitude()))
        print("AP : " + str(apoapsis()))
        print("PE : " + str(periapsis()))
        print(process_resources(resources().all))

    except krpc.error.RPCError as e:
        print("KSP Scene Changed!")
        time.sleep(1)
    except ConnectionAbortedError:
        print("KSP has Disconnected.")
        running = False

    time.sleep(0.1)
    count += 1

