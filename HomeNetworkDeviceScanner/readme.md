## Running the Scanner
 
> **Important:** VS Code (or your terminal) must be run as Administrator.
 
```powershell
python app.py
```
 
Then open your browser and go to:
 
```
http://127.0.0.1:5000
```
 
Click **Scan Network** and wait 20–30 seconds for results.

---
## How It Works
 
1. `scanner.py` uses Scapy to send ARP broadcast packets across your `/24` subnet
2. Devices that respond are collected with their IP and MAC address
3. Each device is enriched with a hostname (via reverse DNS) and vendor name (via [macvendors.com](https://macvendors.com) API)
4. `app.py` runs a Flask server that serves the web UI and exposes two API endpoints:
   - `POST /api/scan` — starts a background scan
   - `GET /api/status` — returns current scan state and results
5. The browser polls `/api/status` every 1.5 seconds until the scan completes

## Notes
 
- Only scans the local `/24` subnet (e.g. `192.168.1.0/24` or `10.0.0.0/24`)
- Does not scan across subnets or the internet
