import os
import subprocess
import sys
import re

def get_wifi_ip():
    result = subprocess.run(["/sbin/ifconfig", "wlan0"], capture_output = True)

    if result.returncode == 0:
        cmd_output = result.stdout.decode()
        ip = get_ip_regex(cmd_output)

        print(ip)
        
    else:
        print("")


def get_lan_ip():
    result = subprocess.run(["/sbin/ifconfig", "eth0"], capture_output = True)

    if result.returncode == 0:
        cmd_output = result.stdout.decode()
        ip = get_ip_regex(cmd_output)

        print(ip)
        
    else:
        print("")

def get_ip_regex(cmd_output):
    pattern = r"inet ([0-9.]+) ?"
    result = re.findall(pattern, cmd_output)

    if result:
        return result[0]

    return ""


if __name__ == "__main__":

    try:
        target = sys.argv[1]

        if target == "wifi":
            get_wifi_ip()
        else:
            get_lan_ip()
            
    except Exception as exp:
        #print(str(exp))
        sys.exit(1)