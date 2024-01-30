#!/usr/bin/python3

import sys
import os
import subprocess

"""
This script is used as listener for power
off button and double click power button for
reseting the whole config of the printer, 
specifically:


DO NOT EDIT OR MODIFY THIS FILE
G3D Software Development Team
"""

dir_path, _ = os.path.split(sys.argv[0])

def main():
    pass

def power_off_delay():
    pass

def power_off_now():
    pass

def reset():
    subprocess.run(["python3", os.path.join(dir_path, "configure_network.py", "G3D-Printer", "g3drocks54321")])

if __name__ == "__main__":
    main()