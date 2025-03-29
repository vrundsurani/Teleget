import scapy.all as scapy
import socket
import platform
import subprocess
import requests
import json
import csv
import speedtest
import nmap
from concurrent.futures import ThreadPoolExecutor

def scan_network(network):
    arp_request = scapy.ARP(pdst=network)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    
    active_ips = [entry[1].psrc for entry in answered_list]
    return active_ips

def check_open_ports(ip, ports=range(1, 65536)):
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            if sock.connect_ex((ip, port)) == 0:
                open_ports.append(port)
    return ip, open_ports

def get_os_info(ip):
    try:
        response = subprocess.check_output(["ping", "-c", "1", ip], stderr=subprocess.DEVNULL)
        return platform.system()
    except:
        return "Unknown"

def get_mac_address(ip):
    try:
        ans, _ = scapy.arping(ip, verbose=False)
        for sent, received in ans:
            return received.hwsrc
    except:
        return "Unknown"

def get_service_info(port):
    services = {22: "SSH", 80: "HTTP", 443: "HTTPS", 3389: "RDP", 8080: "Web Proxy"}
    return services.get(port, "Unknown")

def geolocation_lookup():
    try:
        response = requests.get("https://ipinfo.io/json")
        return response.json()
    except:
        return "Unknown"

def dns_resolution(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unknown"

def run_speed_test():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000
    upload_speed = st.upload() / 1_000_000
    return f"Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps"

def run_vulnerability_scan(ip):
    scanner = nmap.PortScanner()
    scanner.scan(ip, arguments="-sV --script vulners")
    return scanner[ip].get("script", "No vulnerabilities found")

def detect_firewall(ip):
    scanner = nmap.PortScanner()
    scanner.scan(ip, arguments="-Pn")
    return "Firewall Detected" if scanner[ip].state() == "filtered" else "No Firewall"

def sniff_packets():
    print("Starting packet sniffing...")
    packets = scapy.sniff(count=10)
    return packets.summary()

def generate_report(data, filename="scan_results.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["IP Address", "Open Ports", "Operating System", "MAC Address", "Hostname", "Geolocation", "Vulnerabilities", "Network Speed", "Firewall Status", "Packet Sniffing"])
        for entry in data:
            writer.writerow(entry)

def main():
    network = "192.168.1.1/24"  # Change this to your network range
    print(f"Scanning network: {network}")
    
    active_ips = scan_network(network)
    
    print("Discovered IPs:")
    for ip in active_ips:
        print(ip)
    
    print("\nScanning for open ports...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(check_open_ports, active_ips))
    
    geolocation = geolocation_lookup()
    network_speed = run_speed_test()
    packet_sniffing = sniff_packets()
    
    print("\nFetching additional details...")
    report_data = []
    for ip, ports in results:
        os_info = get_os_info(ip)
        mac_address = get_mac_address(ip)
        hostname = dns_resolution(ip)
        service_info = [f"{port} ({get_service_info(port)})" for port in ports]
        vulnerabilities = run_vulnerability_scan(ip)
        firewall_status = detect_firewall(ip)
        report_data.append([ip, ", ".join(service_info), os_info, mac_address, hostname, geolocation, vulnerabilities, network_speed, firewall_status, packet_sniffing])
        print(f"IP: {ip} - OS: {os_info} - MAC: {mac_address} - Hostname: {hostname} - Open Ports: {service_info if service_info else 'None'} - Vulnerabilities: {vulnerabilities} - Firewall: {firewall_status}")
    
    generate_report(report_data)
    print("\nScan results saved to scan_results.csv")

if __name__ == "__main__":
    main()
