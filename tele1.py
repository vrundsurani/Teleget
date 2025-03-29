import hashlib
import requests
import os
import sys
import time
import getpass

# Function to print text in green
def print_green(text):
    print(f"\033[32m{text}\033[0m")

# Display tool credits
def show_credits():
    print_green("\n🔥 Teleget Tool - Made by Vrund 🔥")
    print_green("=" * 40)

# 🔥 VPN & Proxy Detection (Using VPNAPI.io - Free)
VPN_API_KEY = "01d53fcffd654900af37094b0e0ecd92"

def check_vpn(ip):
    try:
        response = requests.get(f"https://vpnapi.io/api/{ip}?key={VPN_API_KEY}")
        data = response.json()
        return data['security']['vpn'] or data['security']['proxy'] or data['security']['tor']
    except:
        return False

# 🔥 Block Bots & Fake Users
def block_bots(user_agent):
    return not user_agent or len(user_agent) < 10

# 🔥 Detect & Block Headless Browsers
def block_headless(navigator):
    return navigator.get("webdriver", False)

# 🔥 Prevent Spam & DDoS Attacks (Too Many Requests Blocker)
refresh_count = 0

def check_refresh_limit():
    global refresh_count
    refresh_count += 1
    if refresh_count > 5:
        return True
    return False

# SHA-256 Hash function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Stored hashed password (hash of "1234")
stored_hashed_password = "14d07d2762f8b6f0b312c105bbe9a27f8578d16381da1317ea0b83939c5d7765"

# Function to verify password with hidden input
def verify_password():
    password = getpass.getpass("Enter password: ")  # This masks the password input
    if hash_password(password) == stored_hashed_password:
        print_green("\n✅ Access Granted!\n")
        return True
    else:
        print_green("\n❌ Access Denied!\n")
        return False

# Function to get Telegram messages
def get_telegram_messages():
    token = input("\nEnter Telegram Bot API Token: ")
    api_url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(api_url)
    data = response.json()
    
    print_green("\n========================")
    if data.get("ok"):
        messages = [f"Message ID: {msg['message']['message_id']}, Text: {msg['message'].get('text', '')}" for msg in data.get("result", []) if "message" in msg]
        print_green("📩 Received Messages:")
        for message in messages:
            print_green(message)
    else:
        print_green("❌ Error fetching updates.")
    print_green("========================\n")

# Function to get bot info
def get_bot_info():
    token = input("\nEnter Telegram Bot API Token: ")
    api_url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(api_url)
    data = response.json()

    print_green("\n========================")
    if data.get("ok"):
        print_green(f"🤖 Bot Info:\n{data}")
    else:
        print_green("❌ Error fetching bot info.")
    print_green("========================\n")

# Function to get chat info
def get_chat_info():
    token = input("\nEnter Telegram Bot API Token: ")
    chat_id = input("Enter Chat ID: ")
    api_url = f"https://api.telegram.org/bot{token}/getChat?chat_id={chat_id}"
    response = requests.get(api_url)
    data = response.json()

    print_green("\n========================")
    if data.get("ok"):
        print_green(f"📜 Chat Info:\n{data}")
    else:
        print_green("❌ Error fetching chat info.")
    print_green("========================\n")

# Function to get chat administrators
def get_chat_admins():
    token = input("\nEnter Telegram Bot API Token: ")
    chat_id = input("Enter Chat ID: ")
    api_url = f"https://api.telegram.org/bot{token}/getChatAdministrators?chat_id={chat_id}"
    response = requests.get(api_url)
    data = response.json()

    print_green("\n========================")
    if data.get("ok"):
        print_green(f"👮 Chat Admins:\n{data}")
    else:
        print_green("❌ Error fetching chat administrators.")
    print_green("========================\n")

# Function to get chat member count
def get_chat_member_count():
    token = input("\nEnter Telegram Bot API Token: ")
    chat_id = input("Enter Chat ID: ")
    api_url = f"https://api.telegram.org/bot{token}/getChatMemberCount?chat_id={chat_id}"
    response = requests.get(api_url)
    data = response.json()

    print_green("\n========================")
    if data.get("ok"):
        print_green(f"👥 Chat Member Count:\n{data}")
    else:
        print_green("❌ Error fetching chat member count.")
    print_green("========================\n")

# Function to send a message
def send_message():
    token = input("\nEnter Telegram Bot API Token: ")
    chat_id = input("Enter Chat ID: ")
    message = input("Enter message: ")
    api_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(api_url)
    data = response.json()

    print_green("\n========================")
    if data.get("ok"):
        print_green("✅ Message sent successfully!")
    else:
        print_green("❌ Error sending message.")
    print_green("========================\n")

# Function to delete a message
def delete_message():
    token = input("\nEnter Telegram Bot API Token: ")
    chat_id = input("Enter Chat ID: ")
    message_id = input("Enter message ID to delete: ")
    api_url = f"https://api.telegram.org/bot{token}/deleteMessage?chat_id={chat_id}&message_id={message_id}"
    response = requests.get(api_url)
    data = response.json()

    print_green("\n========================")
    if data.get("ok"):
        print_green("✅ Message deleted successfully!")
    else:
        print_green("❌ Error deleting message.")
    print_green("========================\n")

# Main function to run the terminal tool
def main():
    show_credits()
    while True:
        print_green("\n🔥 Teleget Tool 🔥")
        print_green("1. Get Telegram Messages")
        print_green("2. Get Bot Info")
        print_green("3. Get Chat Info")
        print_green("4. Get Chat Admins")
        print_green("5. Get Chat Member Count")
        print_green("6. Send Message")
        print_green("7. Delete Message")
        print_green("8. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            if verify_password():
                get_telegram_messages()
        elif choice == "2":
            if verify_password():
                get_bot_info()
        elif choice == "3":
            if verify_password():
                get_chat_info()
        elif choice == "4":
            if verify_password():
                get_chat_admins()
        elif choice == "5":
            if verify_password():
                get_chat_member_count()
        elif choice == "6":
            if verify_password():
                send_message()
        elif choice == "7":
            if verify_password():
                delete_message()
        elif choice == "8":
            print_green("\n👋 Exiting... Have a great day!\n")
            sys.exit()
        else:
            print_green("\n❌ Invalid choice, please try again.\n")

if __name__ == "__main__":
    main()
