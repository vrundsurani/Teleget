import hashlib
import requests
import os
import sys
import time
import getpass

def print_green(text):
    print(f"\033[32m{text}\033[0m")

def input_green(prompt):
    return input(f"\033[32m{prompt}\033[0m")

def getpass_green(prompt):
    return getpass.getpass(f"\033[32m{prompt}\033[0m")

def show_credits():
    print_green("\n🔥 Teleget Pro - Enhanced Telegram Bot Tool 🔥")
    print_green("=" * 50)

VPN_API_KEY = "01d53fcffd654900af37094b0e0ecd92"

def check_vpn(ip):
    try:
        response = requests.get(f"https://vpnapi.io/api/{ip}?key={VPN_API_KEY}")
        data = response.json()
        return data['security']['vpn'] or data['security']['proxy'] or data['security']['tor']
    except:
        return False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

stored_hashed_password = "14d07d2762f8b6f0b312c105bbe9a27f8578d16381da1317ea0b83939c5d7765"

def verify_password():
    password = getpass_green("Enter password: ")
    return hash_password(password) == stored_hashed_password

def get_telegram_messages(token):
    api_url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(api_url)
    return response.json()

def get_bot_info(token):
    api_url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(api_url)
    return response.json()

def get_chat_info(token, chat_id):
    api_url = f"https://api.telegram.org/bot{token}/getChat?chat_id={chat_id}"
    response = requests.get(api_url)
    return response.json()

def get_chat_admins(token, chat_id):
    api_url = f"https://api.telegram.org/bot{token}/getChatAdministrators?chat_id={chat_id}"
    response = requests.get(api_url)
    return response.json()

def get_chat_member_count(token, chat_id):
    api_url = f"https://api.telegram.org/bot{token}/getChatMemberCount?chat_id={chat_id}"
    response = requests.get(api_url)
    return response.json()

def send_message(token, chat_id, message):
    api_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(api_url)
    return response.json()

def delete_message(token, chat_id, message_id):
    api_url = f"https://api.telegram.org/bot{token}/deleteMessage?chat_id={chat_id}&message_id={message_id}"
    response = requests.get(api_url)
    return response.json()

def edit_message(token, chat_id, message_id, new_text):
    api_url = f"https://api.telegram.org/bot{token}/editMessageText?chat_id={chat_id}&message_id={message_id}&text={new_text}"
    response = requests.get(api_url)
    return response.json()

def pin_message(token, chat_id, message_id):
    api_url = f"https://api.telegram.org/bot{token}/pinChatMessage?chat_id={chat_id}&message_id={message_id}"
    response = requests.get(api_url)
    return response.json()

def unpin_message(token, chat_id, message_id):
    api_url = f"https://api.telegram.org/bot{token}/unpinChatMessage?chat_id={chat_id}&message_id={message_id}"
    response = requests.get(api_url)
    return response.json()

def leave_chat(token, chat_id):
    api_url = f"https://api.telegram.org/bot{token}/leaveChat?chat_id={chat_id}"
    response = requests.get(api_url)
    return response.json()

def main():
    show_credits()
    token = input_green("\nEnter Telegram Bot API Token: ")
    
    while True:
        print_green("\n🔥 Teleget Pro 🔥")
        print_green("1. Get Telegram Messages")
        print_green("2. Get Bot Info")
        print_green("3. Get Chat Info")
        print_green("4. Get Chat Admins")
        print_green("5. Get Chat Member Count")
        print_green("6. Send Message")
        print_green("7. Delete Message")
        print_green("8. Edit Message")
        print_green("9. Pin Message")
        print_green("10. Unpin Message")
        print_green("11. Leave Chat")
        print_green("12. Exit")
        
        choice = input_green("\nEnter your choice: ")
        
        if choice == "1" and verify_password():
            print_green(get_telegram_messages(token))
        elif choice == "2" and verify_password():
            print_green(get_bot_info(token))
        elif choice == "3" and verify_password():
            chat_id = input_green("Enter Chat ID: ")
            print_green(get_chat_info(token, chat_id))
        elif choice == "4" and verify_password():
            chat_id = input_green("Enter Chat ID: ")
            print_green(get_chat_admins(token, chat_id))
        elif choice == "5" and verify_password():
            chat_id = input_green("Enter Chat ID: ")
            print_green(get_chat_member_count(token, chat_id))
        elif choice == "6" and verify_password():
            chat_id = input_green("Enter Chat ID: ")
            message = input_green("Enter message: ")
            print_green(send_message(token, chat_id, message))
        elif choice == "7" and verify_password():
            chat_id = input_green("Enter Chat ID: ")
            message_id = input_green("Enter Message ID: ")
            print_green(delete_message(token, chat_id, message_id))
        elif choice == "8" and verify_password():
            chat_id = input_green("Enter Chat ID: ")
            message_id = input_green("Enter Message ID: ")
            new_text = input_green("Enter new text: ")
            print_green(edit_message(token, chat_id, message_id, new_text))
        elif choice == "9" and verify_password():
            chat_id = input_green("Enter Chat ID: ")
            message_id = input_green("Enter Message ID: ")
            print_green(pin_message(token, chat_id, message_id))
        elif choice == "10" and verify_password():
            chat_id = input_green("Enter Chat ID: ")
            message_id = input_green("Enter Message ID: ")
            print_green(unpin_message(token, chat_id, message_id))
        elif choice == "11" and verify_password():
            chat_id = input_green("Enter Chat ID: ")
            print_green(leave_chat(token, chat_id))
        elif choice == "12":
            print_green("\n👋 Exiting... Have a great day!")
            sys.exit()
        else:
            print_green("\n❌ Invalid choice, please try again.")

if __name__ == "__main__":
    main()
