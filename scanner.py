
import ipaddress
from scapy.all import *

#NETWORK INFO
def get_network_info():
    """Get the local network information, such as the IP, MAC, and subnet."""
    iface = str(conf.iface) # what network card am I using?
    local_ip = get_if_addr(iface) # what is my IP on the network card?
    local_mac = get_if_hwaddr(iface) #what is my MAC address
    subnet = str(ipaddress.IPv4Network(f"{local_ip}/24", strict=False)) # take my ip and assume im on /24 network

    
    return iface, local_ip, local_mac, subnet

# ARP SCAN
def arp_scan(subnet, iface):
    """Sends an ARP request to the broadcast address to find all devices on the local network."""
    packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=subnet) # create an ARP request packet
    answered, _ = srp(packet,timeout=3, verbose=False, iface=iface)
    devices = []
    for _, received in answered:
        devices.append({
            'ip': received.psrc,
            'mac': received.hwsrc,
            'hostname': None,
            'vendor': None,         
        })

    devices.sort(key=lambda d: ipaddress.IPv4Address(d['ip'])) # sort devices by IP address
    return devices
