import krpc
import time
import numpy as np
from utils import process_resources

running = True
server = None

while server is None:
    print("Connecting")
    try:
        server = krpc.connect(name ='Controller', address= krpc.DEFAULT_ADDRESS)
    except ConnectionRefusedError: #error raised whe failing to connect to the server.
        print("Server offline")
        time.sleep(2)

time.sleep(2)
print("Started")

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
        
# Set up streams for telemetry
altitude = server.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = server.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
periapsis = server.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
resources = server.add_stream(getattr, vessel, "resources")
srb_fuel = server.add_stream(stage_2_resources.amount, 'SolidFuel')
thrust = server.add_stream(getattr, vessel, "thrust")
mass = server.add_stream(getattr, vessel, "mass")

def twr():
    return thrust()/mass()

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

