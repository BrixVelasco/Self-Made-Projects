import socket
import urllib.request
import urllib.error

def resolve_hostname(ip):
    """Resolve the hostname for a given IP address."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        return "N/A"
    
def get_mac_vendor(mac):
    """Get the vendor name for a given MAC address using the macvendors API."""
    oui = mac.replace(":", "").replace("-", "")[:6] # Get the OUI (first 6 hex digits)
    url = f"https://api.macvendors.com/{oui}"

    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            return resp.read().decode().strip()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "Unknown"
        return "Unknown"
    except Exception:
        return "Unknown"
    
def enrich_devices(devices):
    """Enrich the device information with hostnames and vendor names."""
    for device in devices:
        device['hostname'] = resolve_hostname(device['ip'])
        device['vendor'] = get_mac_vendor(device['mac'])
    return devices

