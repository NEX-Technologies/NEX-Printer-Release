#!/usr/bin/python3

"""
This script simply runs a wifi 
scan and output it to a text file.

The textfile is then read by the main 
program to list in the GUI the
available wifi networks.

This is done so that qt won't have 
a blocking call to a system command.

DO NOT EDIT OR MODIFY THIS FILE
G3D Software Development Team
"""

import subprocess
import sys
import re
import time

def main():

    # Path file where we will save the output.
    text_file_path = sys.argv[1]
   
    while True:

        # Actual command
        command_output = data = subprocess.run(["sudo", "iwlist", "wlan0", "scanning"], capture_output=True)

        # Use regex to get only the SSID.
        pattern = r'ESSID:"(.+?)"'
        result = re.findall(pattern, str(command_output))

        if result:

            # Clear file.
            with open(text_file_path, "w") as f:
                pass

            # Write separated by new line.
            with open(text_file_path, "a") as f:
                for ssid in result:
                    #print(ssid)
                    f.write(ssid + "\n")

        time.sleep(5)

if __name__ == "__main__":
    main()
