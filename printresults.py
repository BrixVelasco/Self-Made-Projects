def print_results(devices, local_ip):
    """Print a formatted table of discovered devices."""
    col_ip       = 18
    col_mac      = 20
    col_hostname = 30
    col_vendor   = 28
 
    header = (
        f"{'IP Address':<{col_ip}}"
        f"{'MAC Address':<{col_mac}}"
        f"{'Hostname':<{col_hostname}}"
        f"{'Vendor':<{col_vendor}}"
    )
    divider = "─" * len(header)
 
    print("\n" + divider)
    print(header)
    print(divider)
 
    for d in devices:
        tag = " ← you" if d["ip"] == local_ip else ""
        print(
            f"{d['ip']:<{col_ip}}"
            f"{d['mac']:<{col_mac}}"
            f"{d['hostname']:<{col_hostname}}"
            f"{d['vendor']:<{col_vendor}}"
            f"{tag}"
        )
 
    print(divider)
    print(f"\n[✓] {len(devices)} device(s) found.\n")