import subprocess

# Define the interface name and IP address information
interface_name = "enp0s3"
ip_address = "192.168.1.100"
netmask = "255.255.255.0"
gateway = "192.168.1.1"

# Set the interface configuration using ifconfig
subprocess.run(['ifconfig', interface_name, ip_address, 'netmask', netmask], check=True)

# Set the default route using the route command
subprocess.run(['route', 'add', 'default', 'gw', gateway, interface_name], check=True)

import subprocess

# Define the interface name and IP address information
interface_name = "enp0s3"
ip_address = "192.168.1.100"
netmask = "255.255.255.0"
gateway = "192.168.1.100"

# Set the interface configuration using ip
subprocess.run(['ip', 'addr', 'add', ip_address + '/' + netmask, 'dev', interface_name], check=True)

# Set the default route using the ip route command
subprocess.run(['ip', 'route', 'add', 'default', 'via', gateway, 'dev', interface_name], check=True)
