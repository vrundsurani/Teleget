import requests
import pyfiglet
import datetime
from termcolor import colored
import threading
import socket
import random
import socks
from requests.exceptions import RequestException
from urllib.parse import urlparse

def banner():
    print(colored(pyfiglet.figlet_format("Subdomain Fuzzer Ultra Pro"), "cyan"))

def load_wordlist(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]

def resolve_dns(subdomain, domain):
    try:
        return socket.gethostbyname(f"{subdomain}.{domain}")
    except socket.gaierror:
        return None

def check_ssl_certificate(subdomain, domain):
    try:
        response = requests.get(f"https://{subdomain}.{domain}", timeout=3, verify=True)
        cert = response.raw.connection.sock.getpeercert()
        return cert
    except RequestException:
        return None

def check_subdomain(domain, subdomain, active_subdomains):
    protocols = ["http", "https"]
    resolved_ip = resolve_dns(subdomain, domain)
    if resolved_ip:
        print(colored(f"[DNS] {subdomain}.{domain} resolves to {resolved_ip}", "blue"))
    for protocol in protocols:
        url = f"{protocol}://{subdomain}.{domain}"
        try:
            response = requests.get(url, timeout=3, headers={"User-Agent": random.choice(user_agents)})
            if response.status_code < 400:
                print(colored(f"[+] Active: {url} ({response.status_code})", "green"))
                active_subdomains.append(url)
                check_ssl_certificate(subdomain, domain)
            else:
                print(colored(f"[-] Dead: {url} ({response.status_code})", "red"))
        except RequestException:
            print(colored(f"[-] Dead: {url}", "red"))

def save_active_subdomains(domain, active_subdomains):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{domain}_{timestamp}.txt"
    with open(filename, "w") as f:
        for sub in active_subdomains:
            f.write(sub + "\n")
    print(colored(f"\n[+] Active subdomains saved in {filename}", "yellow"))

def threaded_scan(domain, wordlist):
    active_subdomains = []
    threads = []
    for sub in wordlist:
        thread = threading.Thread(target=check_subdomain, args=(domain, sub, active_subdomains))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    if active_subdomains:
        save_active_subdomains(domain, active_subdomains)
    else:
        print(colored("No active subdomains found.", "red"))

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

def main():
    banner()
    wordlist_path = input("Enter the path to your wordlist: ")
    domain = input("Enter the target domain (e.g., example.com): ")
    
    wordlist = load_wordlist(wordlist_path)
    threaded_scan(domain, wordlist)

if __name__ == "__main__":
    main()
