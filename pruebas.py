import os
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
interfaz = os.popen('nmcli dev | grep -w "conectado\|connected" | cut -d" " -f1').read()
c = 0
for _ in interfaz.splitlines():
    c += 1
if c > 1:
    print("Interfaces de red en orden!"+bcolors.HEADER+"\nEstas son tus interfaces activas: "+bcolors.ENDC)
    for i in interfaz.splitlines():
        print("\/ " + i + " \/" + os.popen('ifconfig | grep "'+i+'" -A 1 | cut -d" " -f10').read())
    inet = input(bcolors.HEADER + "Selecciona una de las interfaces anteriores para\n"
                           "que sea el encargado de dar IPs a los demás clientes\n"
                           "escribiendo el nombre EXACTO de una de ellas: " + bcolors.ENDC)
    con=0
    while con == 0:
        for i in interfaz.splitlines():
            if inet == i:
                con=1
        inet = input("Error, el nombre NO coincide, vuelve a intentarlo: ")

interfaz1="enp0s3"
print(os.popen('ifconfig | grep '+interfaz1+' -A 1 | cut -d" " -f10').read())