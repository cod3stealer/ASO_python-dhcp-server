import os
import re
import subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def get_subnet(ip):
    subnet_regex = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.')
    subnet_match = subnet_regex.match(ip)
    subnet = subnet_match.group() if subnet_match else None
    return subnet

IP = "12.412.51.2"
sub=get_subnet(IP)
sub = str(sub)
print(sub)
subnet = sub + "0"
print(subnet)
netmask = "255.255.255.0"
range_start = sub + "2"
range_end = sub + "200"