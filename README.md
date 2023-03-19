# ASO PYTHON > DHCP server
## ver documentación del GOOGEL-DRIVE
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
https://ubuntu.com/server/docs/network-configuration
https://linuxhint.com/ubuntu-enable-and-disable-the-network-interface/
"""
To configure a DHCP server in Ubuntu 22.04, you can follow the steps below:
Install the DHCP server package by running the following command in the terminal:
csharp
sudo apt-get install isc-dhcp-server


Once the installation is complete, open the /etc/dhcp/dhcpd.conf configuration file using a text editor of your choice, such as Nano or Vim:
bash
sudo nano /etc/dhcp/dhcpd.conf


Edit the configuration file to specify the network parameters you want to assign through DHCP. For example, you can specify the subnet, default gateway, DNS servers, and lease time. Here's an example configuration:
sql
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.50 192.168.1.100;
    option routers 192.168.1.1;
    option domain-name-servers 8.8.8.8, 8.8.4.4;
    default-lease-time 600;
    max-lease-time 7200;
}
In this example, the DHCP server will assign IP addresses in the range 192.168.1.50 to 192.168.1.100, with a subnet mask of 255.255.255.0. The default gateway will be set to 192.168.1.1, and the DNS servers will be set to Google's public DNS servers (8.8.8.8 and 8.8.4.4). The lease time is set to 10 minutes (600 seconds), and the maximum lease time is 2 hours (7200 seconds).
Save the configuration file and exit the text editor.
Open the /etc/default/isc-dhcp-server file and make sure the INTERFACESv4 variable is set to the network interface you want to use for DHCP. For example, if you want to use the eth0 interface, set the variable as follows:
makefile
INTERFACESv4="eth0"


Save the configuration file and exit the text editor.
Start the DHCP server by running the following command in the terminal:
sql
sudo systemctl start isc-dhcp-server


You can also enable the DHCP server to start automatically at boot time by running the following command:
bash
sudo systemctl enable isc-dhcp-server

