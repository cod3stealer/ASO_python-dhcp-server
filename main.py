# Import de librerias
import os
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

- 

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
        os.popen('sudo apt install isc-dhcp-server')
        print(bcolors.OKGREEN+"Paquete instalado con éxito!\n"+bcolors.ENDC)
    else:
        print(bcolors.OKGREEN+"Tu equipo contiene los paquetes necesarios para que el script funcione!\n"+bcolors.ENDC)

# ! prerequisitos_sockets() comprueba si existen las interfaces de red y si estas están activas
def prerequisitos_sockets():
    algo = os.popen('ip a | cut -d" " -f2 | grep -v -e "^[[:space:]]*$"').read()
    algo = algo.replace(':', '')
    c = 0
    for i in algo.splitlines():
        c += 1
    if c > 2:
        print("Interfaces de red en orden!")
    else:
        print(bcolors.FAIL+"Para lanzar este script es necesario tener dos interfaces de red activas!!"+bcolors.ENDC)
        exit(1)
    # Saber si hay dos sockets activos:
    # Socket DHCP ==> Red Interna, guardar su IP y su nombre en una variable
    # Socket salida INTERNET ==> NAT, guardar su IP y su nombre en una variable

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
    prerequisitos_sockets()
    print("Configurando archivos de servidor...")
    overw("/etc/netplan/01-network-manager-all.yaml",netmanager,"w+","\n")

# Formato de configuración de la interfaz de red DHCP
netmanager = [
    "# Let NetworkManager manage all devices on this system",
    "network:",
    " ethernets:",
    "  enp0s8:",
    "   dhcp4: false",
    "   addresses: [10.0.0.30/24]",
    "   nameservers:",
    "	addresses: [8.8.8.8,8.8.4.4]",
    "  routes:",
    "	- to: default",
    "  	via: 10.0.2.2",
    " version: 2",
    " renderer: NetworkManager"
]
# Formato de archivo para la configuración del socket DHCP
# !!!
# Falta saber como encontrar el nombre del scoket (Ej: enp0s8)
# Falta saber como encontrar la IP del que ejecuta el script (Pos. solución: ip -a | filtrar salida por columnas)
# !!!


__MAIN__()

