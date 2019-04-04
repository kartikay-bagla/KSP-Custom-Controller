import PyCmdMessenger
import time

import krpc
import time
import numpy as np
from utils import process_resources, get_vessel, get_server, get_streams

running = True
server = get_server()

arduino = PyCmdMessenger.ArduinoBoard("COM6",baud_rate=9600)

# Command Descriptions:
    # data_nokia = altitude, apoapsis, periapsis, twr, deltav, g-force
    # data_ard = p_lf, p_ox, p_mp, p_ec
    # data_ksp = throttle, sas, rcs
commands = [["data_nokia","lllfli"],
            ["data_oled","iiii"],
            ["data_ksp","iii"],
            ["error","s"]]

c = PyCmdMessenger.CmdMessenger(arduino, commands)

time.sleep(2)
print("Started")

vessel = get_vessel(server)

altitude, apoapsis, periapsis, resources, g_force, twr = get_streams(server, vessel)

main_resources = ["Oxidizer", "MonoPropellant", "LiquidFuel","ElectricCharge"]

print("Main loop")
while running:
    vals = (int(altitude()), int(apoapsis()), int(periapsis()), twr(), 0, int(g_force()))
    c.send("data_nokia", *vals)
    print("Sent Nokia")

    resources_values = process_resources(resources().all)
    c.send("data_oled", *resources_values)
    print("Sent OLED")

    time.sleep(0.1)