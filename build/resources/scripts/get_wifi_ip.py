#!/usr/bin/python3

import netifaces
import sys

try:
  iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
  output = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
except Exception as exp:
  print("")
  sys.exit(1)

print(output)
sys.exit(0)
