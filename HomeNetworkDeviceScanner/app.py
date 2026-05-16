from flask import Flask, render_template, jsonify
import threading
import helperfunctions
import scanner

app = Flask(__name__)
 
scan_state = {
    "status": "idle",
    "devices": [],
    "network": {}
}
scan_lock = threading.Lock()
 
 
def run_scan():
    global scan_state
    try:
        iface, local_ip, local_mac, subnet = scanner.get_network_info()
 
        with scan_lock:
            scan_state["network"] = {
                "iface": iface,
                "local_ip": local_ip,
                "local_mac": local_mac,
                "subnet": subnet
            }
 
        devices = scanner.arp_scan(subnet, iface)
        devices = helperfunctions.enrich_devices(devices)
 
        for device in devices:
            device["is_you"] = (
                device["ip"] == local_ip or
                device["mac"].lower() == local_mac.lower()
            )
 
        with scan_lock:
            scan_state["devices"] = devices
            scan_state["status"]  = "done"
 
    except Exception as e:
        with scan_lock:
            scan_state["status"]  = "error"
            scan_state["devices"] = []
        print(f"[!] Scan error: {e}")
 
 
@app.route("/")
def index():
    return render_template("index.html")
 
 
@app.route("/api/scan", methods=["POST"])
def start_scan():
    with scan_lock:
        if scan_state["status"] == "scanning":
            return jsonify({"error": "Scan already in progress"}), 409
        scan_state["status"]  = "scanning"
        scan_state["devices"] = []
 
    thread = threading.Thread(target=run_scan, daemon=True)
    thread.start()
    return jsonify({"status": "started"})
 
 
@app.route("/api/status")
def get_status():
    with scan_lock:
        return jsonify(scan_state)
 
 
if __name__ == "__main__":
    print("Starting Network Scanner at http://localhost:5000")
    print("Run this as Administrator for ARP scanning to work!")
    app.run(debug=False, port=5000)