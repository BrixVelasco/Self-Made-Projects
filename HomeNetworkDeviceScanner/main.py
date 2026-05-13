from scanner import *
from helperfunctions import *
from printresults import *

def main():
    print("=" * 60)
    print("       HOME NETWORK DEVICE SCANNER")
    print("=" * 60)
 
    # 1. Get network info
    iface, local_ip, local_mac, subnet = get_network_info()
    print(f"  Interface : {iface}")
    print(f"  Your IP   : {local_ip}")
    print(f"  Your MAC  : {local_mac}")
    print(f"  Subnet    : {subnet}")
 
    # 2. ARP scan
    devices = arp_scan(subnet, iface)
 
    if not devices:
        print("[!] No devices found. Make sure you're running as Administrator.")
        return
 
    # 3. Enrich with hostname + vendor
    print(f"[*] Found {len(devices)} device(s). Resolving hostnames and vendors...")
    devices = enrich_devices(devices)
 
    # 4. Print results
    print_results(devices, local_ip)
 
 
if __name__ == "__main__":
    main()
