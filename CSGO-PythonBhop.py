# CSGO-PythonBhop
# Simple CSGO Bunnyhop hack
# Works with Python 3.9.5
# Copyright Lunarixus (C) 2021

import pymem
import pymem.process
import time
import keyboard
import re

# Signature calculating function
def get_sig(modname, pattern, extra = 0, offset = 0, relative = True):
    pm = pymem.Pymem('csgo.exe')
    module = pymem.process.module_from_name(pm.process_handle, modname)
    bytes = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
    match = re.search(pattern, bytes).start()
    out = pm.read_int(module.lpBaseOfDll + match + offset) + extra
    if relative:
        print("[*] Got address of", pattern, "at 0x{:X}".format(out - module.lpBaseOfDll))
    else:
        print("[*] Got address of", pattern, "at 0x{:X}".format(out))
    return out - module.lpBaseOfDll if relative else out

# Signatures as of 19/07/2021
print("[*] Dynamically updating offsets...")
dwLocalPlayer = get_sig('client.dll', rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF', 4, 3)
dwForceJump = get_sig('client.dll', rb'\x8B\x0D....\x8B\xD6\x8B\xC1\x83\xCa\x02', 0, 2)
m_fFlags = 0x104

# Variables
GoDown = 4
GoUp = 5

# Calculate addresses
cs_process = pymem.Pymem( "csgo.exe" )
client_base = pymem.process.module_from_name(cs_process.process_handle, "client.dll").lpBaseOfDll
localplayeraddress = cs_process.read_int(client_base + dwLocalPlayer)

# Print some information
print("[*] CS:GO PID is", cs_process.process_id)
print("[*] dwLocalPlayer is at", hex(localplayeraddress))

# Start loop for hack
while True:
    if keyboard.is_pressed('space'):
        flags_val = cs_process.read_int(localplayeraddress + m_fFlags)
        print(flags_val)
        
        if flags_val == 256:
            cs_process.write_int(client_base + dwForceJump, GoDown)
        else:
            cs_process.write_int(client_base + dwForceJump, GoUp)
