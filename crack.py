import os
import subprocess
import threading
import itertools
import time
import hashlib
import sqlite3
from tqdm import tqdm
from multiprocessing import Pool

def check_7zip():
    """Check if 7-Zip is installed."""
    if subprocess.run(["which", "7z"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
        print("7-Zip not installed!")
        exit(1)

def get_input(prompt):
    """Get user input and check file existence."""
    while True:
        path = input(prompt).strip()
        if os.path.exists(path):
            return path
        print("File not found! Try again.")

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
            print(f"\nSuccess! Password Found: {password}")
            log_attempt(password, True)
            success = True
            exit(0)
        log_attempt(password, False)
    
    print("Cracking...")
    with Pool(processes=os.cpu_count()) as pool:
        list(tqdm(pool.imap(worker, passwords), total=len(passwords), desc="Progress"))
    
    if not success:
        print("\nShitty wordlist, dumbass!")
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
    print(f"Generated wordlist saved as {filename}")
    return filename

def brute_force_mode(length, charset):
    """Brute-force mode: Generate and test all possible combinations."""
    print("Starting brute-force mode...")
    for attempt in itertools.product(charset, repeat=length):
        password = "".join(attempt)
        if attempt_extract(archive, password):
            print(f"Success! Password Found: {password}")
            exit(0)
    print("Brute-force failed.")

def main():
    """Main function to execute the script."""
    check_7zip()
    archive = get_input("Enter Archive: ")
    mode = input("Choose mode - Dictionary (d) or Brute Force (b): ").strip().lower()
    
    if mode == 'd':
        choice = input("Do you have a wordlist? (y/n): ").strip().lower()
        if choice == 'y':
            wordlist = get_input("Enter Wordlist: ")
        else:
            base_word = input("Enter base word to generate wordlist: ").strip()
            wordlist = generate_wordlist(base_word)
        crack_password(archive, wordlist)
    elif mode == 'b':
        length = int(input("Enter password length: ").strip())
        charset = input("Enter character set (e.g., abc123!@#): ").strip()
        brute_force_mode(length, charset)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
