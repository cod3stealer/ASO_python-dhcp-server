# Import de librerias
import os
import re
import subprocess

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

# @Funciones:

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
        os.popen('sudo apt-get install isc-dhcp-server -y')
        print(bcolors.OKGREEN + "Paquete DHCP-server instalado con éxito!\n" + bcolors.ENDC)
    elif "net-tools" not in control:
        os.popen('sudo apt-get install net-tools')
        print(bcolors.OKGREEN+"Paquete NET-TOOLS instalado con éxito!\n"+bcolors.ENDC)
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

        print(bcolors.HEADER + "\n\nLa interfaz se ha recogido correctamente:\n" + bcolors.HEADER + inet_dhcp + bcolors.ENDC + "\nCon IP" + bcolors.HEADER + os.popen(
                'ifconfig | grep ' + inet_dhcp + ' -A 1 | cut -d" " -f10').read() + bcolors.ENDC+bcolors.HEADER+"\nAHORA, selecciona una de las interfaces anteriores para que sea el encargado de dar conectividad a Internet\n"
                               "a los clientes escribiendo el nombre EXACTO de una de ellas." + bcolors.ENDC)

        interfaz = os.popen('nmcli dev | grep -v '+inet_dhcp+' | grep -w "conectado\|desconectado\|connected\|disconnected" | cut -d" " -f1,5').read()

        for i in interfaz.splitlines():
            print("\/ " + i + " \/" + os.popen('ifconfig | grep "' + i + '" -A 1 | cut -d" " -f10').read())
        print("AVISO: si escoges una interfaz de red desconectada, esta se activará automáticamente")

        interfaz = os.popen('nmcli dev | grep -v "' + inet_dhcp + '" | grep -w "conectado\|desconectado\|connected\|disconnected" | cut -d" " -f1').read()
        con = 0
        while con == 0:
            inet_internet = input("=> ")
            for i in interfaz.splitlines():
                if inet_internet == i:
                    con = 1

        # Cambio de estado de las interfaces
        result = os.popen('ip link show '+inet_internet+' up').read()
        if result == "":
            result = os.popen('ip link set '+inet_internet+' up').read()
            if result != 0:
                print(f"Error en: {inet_internet}.")
                exit(1)

        # Configuracion IP
        ip_internet = "192.168.71.1"
        os.popen('sudo ip addr flush dev '+inet_internet)
        result = os.popen('sudo ip addr add '+ip_internet+'/24 dev '+inet_internet).read()
        if result != "":
            print(f"Error: IP {ip_internet} en {inet_internet}.")
            exit(1)

        print(f"IP de {inet_internet} cambiada a {ip_internet}.")
        print(os.popen('ifconfig | grep "' + inet_internet + '" -A 1 | cut -d" " -f1,10').read())

        return inet_dhcp,inet_internet
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

# ! set_dhcp_conf() establece el rango de IPs dadas por el DHCP
def set_dhcp_conf(IP):
    sub=get_subnet(IP)
    subnet = sub + "0"
    netmask = "255.255.255.0"
    range_start = sub + "2"
    range_end = sub + "200"
    gateway =  IP
    dns_servers = ["8.8.8.8", "8.8.4.4"]
    default_lease="600"
    max_time="7200"

    subprocess.run(["sudo", "cp", "/etc/dhcp/dhcpd.conf", "/etc/dhcp/dhcpd.conf.bak"])

    with open("/etc/dhcp/dhcpd.conf", "w") as f:
        f.write("default-lease-time {};\n".format(default_lease))
        f.write("max-lease-time {};\n".format(max_time))
        f.write("authoritative;")
        f.write("subnet {} netmask {} {\n".format(subnet, netmask))
        f.write("range {} {};\n".format(range_start, range_end))
        f.write("option routers {};\n".format(gateway))
        f.write("option domain-name-servers {};\n}".format(", ".join(dns_servers)))

    os.popen('sudo systemctl start isc-dhcp-server')
    os.popen('sudo systemctl enable isc-dhcp-server')
    os.popen('sudo systemctl status isc-dhcp-server')
    os.popen('sudo netplan apply')
    allow_ufw()

# ! get_subnet() saca la subnet de máscara 24 de cualquier IP
def get_subnet(ip):
    subnet_regex = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.')
    subnet_match = subnet_regex.match(ip)
    subnet = subnet_match.group() if subnet_match else None
    return subnet

# ! allow_ufw() permite el puerto DHCP para que funciones
def allow_ufw():
    os.popen('sudo ufw allow  67/udp').read()

# ! overw() sobreescribe ficheros:
def overw(fil,word,wrx,adds):
    file = open(fil, wrx)
    for i in word:
        file.write(i + adds)
    file.close()
    # fil = ruta del fichero
    # word = cadenas de texto
    # wrx = acción que se quiere realizar
    # adds = opción

# ! set_static_dhcp() modifica Netplan para que esté establezca el servidor DHCP con IP estática
def set_static_dhcp(net,inet,inet_internet):
    netmanager = [
        "# Let NetworkManager manage all devices on this system",
        "network:",
        " ethernets:",
        "  " + inet + ":",
        "   dhcp4: false",
        "   addresses: [" + net + "/24]",
        "   nameservers:",
        "	  addresses: [8.8.8.8,8.8.4.4]",
        "  routes:",
        "	- to: default",
        "  	  via: "+inet_internet,
        " version: 2",
        " renderer: NetworkManager"
    ]
    overw("/etc/netplan/01-network-manager-all.yaml", netmanager, "w+", "\n")
    os.popen('sudo netplan apply')


# ! __MAIN__() función principal del script
def __MAIN__():
    root()
    print("Comprobando requisitos previos...")
    prerequisitos_dhcp()
    print("Comprando interfaces de red...")
    inet = prerequisitos_sockets()
    IP = os.popen('ifconfig | grep ' + inet[0] + ' -A 1 | cut -d" " -f10').read()
    set_inetv4(inet[0])
    set_static_dhcp(IP,inet[0],inet[1])
    set_dhcp_conf(IP)

__MAIN__()
