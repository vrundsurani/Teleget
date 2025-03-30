import os
import subprocess
import itertools
import time
import sqlite3
from tqdm import tqdm
from multiprocessing import Pool
from colorama import Fore, Style

def check_7zip():
    """Check if 7-Zip is installed on Kali Linux."""
    if subprocess.run(["which", "7z"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
        print(Fore.RED + "[!] 7-Zip not installed! Installing 7-Zip..." + Style.RESET_ALL)
        try:
            subprocess.run(["sudo", "apt-get", "install", "p7zip-full", "-y"], check=True)
            print(Fore.GREEN + "[+] 7-Zip installed successfully!" + Style.RESET_ALL)
        except subprocess.CalledProcessError:
            print(Fore.RED + "[!] Failed to install 7-Zip. Please install it manually." + Style.RESET_ALL)
            exit(1)

def get_input(prompt):
    """Get user input and check file existence."""
    while True:
        path = input(Fore.GREEN + prompt + Style.RESET_ALL).strip()
        if os.path.exists(path):
            return path
        print(Fore.RED + "[!] File not found! Try again." + Style.RESET_ALL)

def attempt_extract(archive, password):
    """Attempt to extract the archive with a given password."""
    command = ["7z", "x", f"-p{password}", archive, "-o" + "cracked", "-y"]
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def log_attempt(password, success):
    """Log password attempts to a database."""
    conn = sqlite3.connect("crack_log.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS attempts (password TEXT, success INTEGER)")
    cursor.execute("INSERT INTO attempts (password, success) VALUES (?, ?)", (password, int(success)))
    conn.commit()
    conn.close()

def crack_password(archive, wordlist):
    """Try passwords from the wordlist using multiprocessing."""
    success = False
    with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
        passwords = [line.strip() for line in f]
    
    def worker(password):
        nonlocal success
        if success:
            return
        if attempt_extract(archive, password):
            print(Fore.GREEN + f"\nSuccess! Password Found: {password}" + Style.RESET_ALL)
            log_attempt(password, True)
            success = True
            exit(0)
        log_attempt(password, False)
    
    print(Fore.CYAN + "Cracking..." + Style.RESET_ALL)
    with Pool(processes=os.cpu_count()) as pool:
        list(tqdm(pool.imap(worker, passwords), total=len(passwords), desc="Progress"))
    
    if not success:
        print(Fore.RED + "\nShitty wordlist, dumbass!" + Style.RESET_ALL)
        exit(1)

def generate_wordlist(base_word):
    """Generate a wordlist with common variations."""
    variations = set()
    common_substitutions = {
        "a": ["@", "4"],
        "e": ["3"],
        "i": ["1", "!"]
    }
    for i in range(1, len(base_word) + 1):
        for perm in itertools.permutations(base_word, i):
            word = "".join(perm)
            variations.add(word)
            for char, subs in common_substitutions.items():
                for sub in subs:
                    variations.add(word.replace(char, sub))
    filename = "generated_wordlist.txt"
    with open(filename, 'w') as f:
        for word in variations:
            f.write(word + "\n")
    print(Fore.CYAN + f"Generated wordlist saved as {filename}" + Style.RESET_ALL)
    return filename

def brute_force_mode(archive, length, charset):
    """Brute-force mode: Generate and test all possible combinations."""
    print(Fore.CYAN + "Starting brute-force mode..." + Style.RESET_ALL)
    for attempt in itertools.product(charset, repeat=length):
        password = "".join(attempt)
        if attempt_extract(archive, password):
            print(Fore.GREEN + f"Success! Password Found: {password}" + Style.RESET_ALL)
            exit(0)
    print(Fore.RED + "Brute-force failed." + Style.RESET_ALL)

def main():
    """Main function to execute the script."""
    os.system('clear')
    print(Fore.MAGENTA + "=== Cracker ===" + Style.RESET_ALL)
    print(Fore.YELLOW + "Welcome to Cracker! Your 7-Zip password cracking tool for Kali Linux." + Style.RESET_ALL)
    check_7zip()
    archive = get_input("Enter Archive: ")
    mode = input(Fore.YELLOW + "Choose mode - Dictionary (d) or Brute Force (b): " + Style.RESET_ALL).strip().lower()
    
    if mode == 'd':
        choice = input(Fore.YELLOW + "Do you have a wordlist? (y/n): " + Style.RESET_ALL).strip().lower()
        if choice == 'y':
            wordlist = get_input("Enter Wordlist: ")
        else:
            base_word = input(Fore.YELLOW + "Enter base word to generate wordlist: " + Style.RESET_ALL).strip()
            wordlist = generate_wordlist(base_word)
        crack_password(archive, wordlist)
    elif mode == 'b':
        length = int(input(Fore.YELLOW + "Enter password length: " + Style.RESET_ALL).strip())
        charset = input(Fore.YELLOW + "Enter character set (e.g., abc123!@#): " + Style.RESET_ALL).strip()
        brute_force_mode(archive, length, charset)
    else:
        print(Fore.RED + "[!] Invalid choice." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
