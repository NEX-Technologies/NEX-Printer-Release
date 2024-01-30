#!/usr/bin/python3

import sys
import os
import subprocess

"""
This script is used for configuring network
settings using parameters/keyword passed
specifically by:
                                                                        Keyword

- Changing hotspot mode to Wi-Fi mode with SSID and pass.               [wifi]
- Changing from Wi-Fi mode to hotspot mode.                             [hotspot]
- Connecing to a Wi-Fi using SSID and password.                         Same as [wifi]
- Changing hotspot credentials.                                         Same as [hotspot]
- Resettings all network settings to default.                           [reset]

The number on the right above indicates the action to
be done as passed in this script via command line
arguments.

Usage:
- Change hotspot mode to wifi mode or connecting to wifi:               python3 wifi wifi_ssid wifi_password
- Change wifi mode to hotspot mode or changing hotspot credentials:     python3 hotspot hotspot_ssid hotspot_password
- Reset network settings:                                               python3 reset

DO NOT EDIT OR MODIFY THIS FILE
G3D Software Development Team
"""

# Switching between wifi and hotspot mode in Raspberry Pi
# requires to edit a file /etc/dhcpcd.conf. To enable
# or disable it, we just need to disbale/enable hostapd service
# and commenting and uncommenting the hotspot config in 
# /etc/dhcpcd.conf contained in the variables below.

HOTSPOT_MODE_CONFIG = """# A sample configuration for dhcpcd.
# See dhcpcd.conf(5) for details.

# Allow users of this group to interact with dhcpcd via the control socket.
#controlgroup wheel

# Inform the DHCP server of our hostname for DDNS.
hostname

# Use the hardware address of the interface for the Client ID.
clientid
# or
# Use the same DUID + IAID as set in DHCPv6 for DHCPv4 ClientID as per RFC4361.
# Some non-RFC compliant DHCP servers do not reply with this set.
# In this case, comment out duid and enable clientid above.
#duid

# Persist interface configuration when dhcpcd exits.
persistent

# Rapid commit support.
# Safe to enable by default because it requires the equivalent option set
# on the server to actually work.
option rapid_commit

# A list of options to request from the DHCP server.
option domain_name_servers, domain_name, domain_search, host_name
option classless_static_routes
# Respect the network MTU. This is applied to DHCP routes.
option interface_mtu

# Most distributions have NTP support.
#option ntp_servers

# A ServerID is required by RFC2131.
require dhcp_server_identifier

# Generate SLAAC address using the Hardware Address of the interface
#slaac hwaddr
# OR generate Stable Private IPv6 Addresses based from the DUID
slaac private

# Example static IP configuration:
#interface eth0
#static ip_address=192.168.0.10/24
#static ip6_address=fd51:42f8:caae:d92e::ff/64
#static routers=192.168.0.1
#static domain_name_servers=192.168.0.1 8.8.8.8 fd51:42f8:caae:d92e::1

# It is possible to fall back to a static IP if DHCP fails:
# define static profile
#profile static_eth0
#static ip_address=192.168.1.23/24
#static routers=192.168.1.1
#static domain_name_servers=192.168.1.1

# fallback to static profile on eth0
#interface eth0
#fallback static_eth0

# G3DEdit - For hotspot.
interface wlan0
static ip_address=192.168.4.1/24
nohook wpa_supplicant
"""

WIFI_MODE_CONFIG = """# A sample configuration for dhcpcd.
# See dhcpcd.conf(5) for details.

# Allow users of this group to interact with dhcpcd via the control socket.
#controlgroup wheel

# Inform the DHCP server of our hostname for DDNS.
hostname

# Use the hardware address of the interface for the Client ID.
clientid
# or
# Use the same DUID + IAID as set in DHCPv6 for DHCPv4 ClientID as per RFC4361.
# Some non-RFC compliant DHCP servers do not reply with this set.
# In this case, comment out duid and enable clientid above.
#duid

# Persist interface configuration when dhcpcd exits.
persistent

# Rapid commit support.
# Safe to enable by default because it requires the equivalent option set
# on the server to actually work.
option rapid_commit

# A list of options to request from the DHCP server.
option domain_name_servers, domain_name, domain_search, host_name
option classless_static_routes
# Respect the network MTU. This is applied to DHCP routes.
option interface_mtu

# Most distributions have NTP support.
#option ntp_servers

# A ServerID is required by RFC2131.
require dhcp_server_identifier

# Generate SLAAC address using the Hardware Address of the interface
#slaac hwaddr
# OR generate Stable Private IPv6 Addresses based from the DUID
slaac private

# Example static IP configuration:
#interface eth0
#static ip_address=192.168.0.10/24
#static ip6_address=fd51:42f8:caae:d92e::ff/64
#static routers=192.168.0.1
#static domain_name_servers=192.168.0.1 8.8.8.8 fd51:42f8:caae:d92e::1

# It is possible to fall back to a static IP if DHCP fails:
# define static profile
#profile static_eth0
#static ip_address=192.168.1.23/24
#static routers=192.168.1.1
#static domain_name_servers=192.168.1.1

# fallback to static profile on eth0
#interface eth0
#fallback static_eth0
"""

# The variables below are the files needed
# to be edited to change the SSID and password
# of Wi-Fi and/or hotspot.
WPA_SUPPLICANT_CONTENTS = """ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=PH

network={
        ssid="<ssid>"
        psk="<password>"
        key_mgmt=WPA-PSK
}
"""

HOSTAPD_CONTENTS = """country_code=PH
interface=wlan0
hw_mode=g
channel=7
macaddr_acl=0
auth_algs=1
ssid=<ssid>
wpa=2
wpa_passphrase=<password>
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
"""

def main():
    # If there is at least one parameters sent, we 
    # continue checking the command.
    if len(sys.argv) > 1:

        command = sys.argv[1]
        
        
        print("[DEBUG] Command received: {}".format(command))

        if command == "wifi":

            # Change mode from hotspot to wifi
            # or connect to wifi.

            ssid = sys.argv[2]
            password = sys.argv[3]

            hotspot_to_wifi(ssid, password)

        elif command == "hotspot":

            # Change mode from wifi to hotspot
            # or change hotspot credentials.

            ssid = sys.argv[2]
            password = sys.argv[3]

            wifi_to_hospot(ssid, password)


        elif command == "reset":
            pass
    else:
        print("[DEBUG] No parameters received.")
        
def hotspot_to_wifi(ssid, password):
    """
    This function runs a command and change 
    contents of the file to activate wifi.
    Then it changes the credential of
    the SSID and password of the wifi config 
    file.
    """
    
    print("[DEBUG] Hotspot to Wi-Fi or Connect to Wi-Fi")
    print("[DEBUG] SSID: {}".format(ssid))
    print("[DEBUG] Password: {}".format(password))

    # First we run the command to disable the hostapd.service
    # then we edit the /etc/dhcpcd.conf config file to disable
    # hotspot and enable wifi.

    result = subprocess.run(["sudo", "systemctl", "disable", "hostapd.service", "dnsmasq.service"])
    
    if result.returncode == 0:
        print("[DEBUG] Success. Disabled hostapd and dnsmasq.")
        
        with open("/etc/dhcpcd.conf", "w") as f:
            f.write(WIFI_MODE_CONFIG)
            print("[DEBUG] /etc/dhcpcd.conf edited.")

        # Then we edit the config file for wifi to 
        # change to the desired SSID and password.
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as f:
            f.write(WPA_SUPPLICANT_CONTENTS.replace("<ssid>", ssid).replace("<password>",password))
            print("[DEBUG] /etc/wpa_supplicant/wpa_supplicant.conf edited.")
            
        # Restart the wlan configuration.
        result = subprocess.run(["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"])

        if result.returncode == 0:
            print("[DEBUG] Success. Restarted wlan0.")
    
    else:
        print("[DEBUG] Failed to disable hostapd and dnsmasq")

def wifi_to_hospot(ssid, password):
    """
    This function runs a command and change 
    contents of the file to activate hotspot.
    Then it changes the credential of
    the SSID and password of the hotspot config 
    file.
    """
    
    print("[DEBUG] Wi-Fi to Hotspot or Change Hotspot Credential")
    print("[DEBUG] SSID: {}".format(ssid))
    print("[DEBUG] Password: {}".format(password))

    # First we run the command to enable the hostapd.service
    # then we edit the /etc/dhcpcd.conf config file to enable
    # wifi and disable hotspot

    result = subprocess.run(["sudo", "systemctl", "enable", "hostapd.service", "dnsmasq.service"])
  
    if result.returncode == 0:
        print("[DEBUG] Success. Enabled hostapd and dnsmasq.")
        
        with open("/etc/dhcpcd.conf", "w") as f:
            f.write(HOTSPOT_MODE_CONFIG)
            print("[DEBUG] /etc/dhcpcd.conf edited.")

        # Then we edit the config file for hotspot to 
        # change to the desired SSID and password.
        with open("/etc/hostapd/hostapd.conf", "w") as f:
            f.write(HOSTAPD_CONTENTS.replace("<ssid>", ssid).replace("<password>",password))
            print("[DEBUG] /etc/hostapd/hostapd.conf edited.")
            
    else:
        print("[DEBUG] Failed to enable hostapd and dnsmasq.")

def reset_network():
    """
    This function resets every network settings, particularly:
    - Reset back to hotspot mode.
    - Change SSID and password of hotspot to default.
    """
    wifi_to_hospot("G3D-Printer", "g3dRocks54321")

if __name__ == "__main__":
    main()

