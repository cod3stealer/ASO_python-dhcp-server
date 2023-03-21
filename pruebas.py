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

        # Bring up the interface if it's not up
        result = os.popen('ip link show '+inet_internet+' up').read()
        if result == "":
            result = os.popen('ip link set '+inet_internet+' up').read()
            if result != 0:
                print(f"Error en: {inet_internet}.")
                exit(1)

        # Configure the IP address
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

inet = prerequisitos_sockets()
