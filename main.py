# Import de librerias
import os
import subprocess
import re
"""
Progresión del programa:

- * Comprobación de permisos de superusuario

- * Comprobación de los requisitos mínimos para desplegar un servidor DHCP

- ! Comprobación de sockets ==> Es necesario tener dos sockets activos:  
> uno en red interna (socket DHCP) y otro NAT (socket salida INTERNET)

- ! Configuración de NETPLANS: 
> Formato hecho y guardado en la variable netmanager.
> Falta guardar en una variable la IP del que ejecuta el script
> y como averiguar el nombre del socket que funcionará 
> como socket DHCP
"""
# Class con diferentes estilos para los diferentes outputs.
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

# Funciones:

# ! root() trae información sobre si el script está siendo ejecutado como administrador
def root():
    if os.geteuid() != 0:
        print(bcolors.WARNING + "Para ejecutar este script son necesarios los permisos de superusuario o 'root'!" + bcolors.ENDC)
        exit(1)

# ! prerequisitos() comprueba que el paquete de Linux DHCP-server está instalado
def prerequisitos_dhcp():
    control = os.popen('dpkg-query -l').read()
    if "isc-dhcp-server" not in control:
        print(bcolors.BOLD+"Tu equipo no cuenta con el paquete de Linux - 'isc-dhcp-server' - "
              "\nEl paquete se está instalando automáticamente..."+bcolors.ENDC)
        os.popen('sudo apt-get install isc-dhcp-server')
        print(bcolors.OKGREEN+"Paquete instalado con éxito!\n"+bcolors.ENDC)
    else:
        print(bcolors.OKGREEN+"Tu equipo contiene los paquetes necesarios para que el script funcione!\n"+bcolors.ENDC)

# ! prerequisitos_sockets() comprueba si existen las interfaces de red y si estas están activas
def prerequisitos_sockets():
    interfaz = os.popen('nmcli dev | grep -w "conectado\|connected" | cut -d" " -f1').read()
    c = 0
    for _ in interfaz.splitlines():
        c += 1
    if c > 1:
        print("Interfaces de red en orden!" + bcolors.HEADER + "\nEstas son tus interfaces activas: " + bcolors.ENDC)
        for i in interfaz.splitlines():
            print("\/ " + i + " \/" + os.popen('ifconfig | grep "' + i + '" -A 1 | cut -d" " -f10').read())
        print(bcolors.HEADER + "Selecciona una de las interfaces anteriores para\n"
                               "que sea el encargado de dar IPs a los demás clientes\n"
                               "escribiendo el nombre EXACTO de una de ellas" + bcolors.ENDC)
        con = 0
        while con == 0:
            inet_dhcp = input("=> ")
            for i in interfaz.splitlines():
                if inet_dhcp == i:
                    con = 1
        print("Has seleccionado como interfaz de red DHCP:\n" + bcolors.HEADER + inet_dhcp + bcolors.ENDC + "\nCon IP" + bcolors.HEADER + os.popen(
                'ifconfig | grep ' + inet_dhcp + ' -A 1 | cut -d" " -f10').read() + bcolors.ENDC)
        return inet_dhcp
    else:
        print(bcolors.FAIL+"Para lanzar este script es necesario tener dos interfaces de red activas!!"+bcolors.ENDC)
        exit(1)
    # Saber si hay dos sockets activos:
    # Socket DHCP ==> Red Interna, guardar su IP y su nombre en una variable
    # Socket salida INTERNET ==> NAT, guardar su IP y su nombre en una variable

# ! set_inetv4() establece la interfaz que dará IPs
def set_inetv4(interfaz):
    print("Configurando archivos de servidor...")
    with open('/etc/default/isc-dhcp-server', 'w', encoding='utf-8') as file:
        file.write('INTERFACESv4="' + interfaz + '"\nINTERFACESv6=""')

def set_dhcp_conf(IP):
    sub=get_subnet(IP)
    sub+="0"
    subnet = sub
    sub-="0"
    netmask = "255.255.255.0"
    sub+="2"
    range_start = sub
    sub-="2"
    sub+="253"
    range_end = sub
    sub-="253"
    sub+="1"
    gateway = sub
    dns_servers = ["8.8.8.8", "8.8.4.4"]
    default-lease-time="600"
    max-lease-time="7200"

    subprocess.run(["sudo", "cp", "/etc/dhcp/dhcpd.conf", "/etc/dhcp/dhcpd.conf.bak"])

    with open("/etc/dhcp/dhcpd.conf", "w") as f:
        f.write("authoritative;")
        f.write("subnet {} netmask {} {\n".format(subnet, netmask))
        f.write("range {} {};\n".format(range_start, range_end))
        f.write("option routers {};\n".format(gateway))
        f.write("option domain-name-servers {};\n".format(", ".join(dns_servers)))
        f.write("default-lease-time {};\n".format(default-lease-time))
        f.write("max-lease-time {};\n}".format(max - lease - time))
    os.chmod("/etc/dhcp/dhcpd.conf", 0o644)

def get_subnet(ip):
    subnet_regex = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.')
    subnet_match = subnet_regex.match(ip)
    subnet = subnet_match.group() if subnet_match else None
    return subnet

def allow_ufw():
    os.popen('sudo ufw allow  67/udp').read()
# ! overw() sobreescribe ficheros:
# fil = ruta del fichero
# word = cadenas de texto
# wrx = acción que se quiere realizar
# adds = opción
def overw(fil,word,wrx,adds):
    file = open(fil, wrx)
    for i in word:
        file.write(i + adds)
    file.close()

# ! __MAIN__() función principal del script
def __MAIN__():
    root()
    print("Comprobando requisitos previos...")
    prerequisitos_dhcp()
    print("Comprando interfaces de red...")
    inet_dhcp = prerequisitos_sockets()
    IP = os.popen('ifconfig | grep ' + inet_dhcp + ' -A 1 | cut -d" " -f10').read()
    set_inetv4(inet_dhcp)
    set_dhcp_conf(IP)
    overw("/etc/netplan/01-network-manager-all.yaml",netmanager,"w+","\n")

# Formato de configuración de la interfaz de red DHCP
netmanager = [
    "# Let NetworkManager manage all devices on this system",
    "network:",
    " ethernets:",
    "  "+inet_dhcp+":",
    "   dhcp4: false",
    "   addresses: ["+IP+"/24]",
    "   nameservers:",
    "	addresses: [8.8.8.8,8.8.4.4]",
    "  routes:",
    "	- to: default",
    "  	via: 10.0.2.2",
    " version: 2",
    " renderer: NetworkManager"
]

__MAIN__()

