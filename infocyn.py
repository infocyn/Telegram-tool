#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Username Tool — by infocyn

import os, sys, time, random, string, webbrowser
from os import path, system
from base64 import b64decode
from datetime import datetime

try:
    from requests import get
except ImportError:
    system('pip install requests')
    from requests import get

try:
    from telethon import TelegramClient, sync, errors, functions, types
    from telethon.tl.functions.account import CheckUsernameRequest, UpdateUsernameRequest
except ImportError:
    system('pip install telethon')
    from telethon import TelegramClient, sync, errors, functions, types
    from telethon.tl.functions.account import CheckUsernameRequest, UpdateUsernameRequest

try:
    from bs4 import BeautifulSoup as S
except ImportError:
    system('pip install beautifulsoup4')
    from bs4 import BeautifulSoup as S

try:
    from fake_useragent import UserAgent
except ImportError:
    system('pip install fake_useragent')
    from fake_useragent import UserAgent

# --------------------- Colors ---------------------
RED = '\033[1;31m'
YELLOW = '\033[1;33m'
GREEN = '\033[1;32m'
CYAN = '\033[1;36m'
MAG = '\033[35m'
RESET = '\033[0m'
BOLD = '\033[1m'

# --------------------- Global ---------------------
USERNAME = "@infocyn"
COUNT = 1
LAST_GENERATED = []

# --------------------- ASCII Hook ---------------------
HOOK = r"""
             _
           _| |_
         _|  |  |_
        |  \ | /  |
         \  \|/  /
          \  |  /
           \ | /
            \|/
             V   🎣  # Rare Username Fishing Tool
"""

# --------------------- Welcome Screen ---------------------
def welcome_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Visual banner
    banner = f"{RED}◢◤◢◤  infocyn ◢◤◢◤{RESET}\n"
    for char in banner:
        print(char, end='', flush=True)
        time.sleep(0.005)
    
    # Welcome message
    welcome_msg = f"{CYAN}Welcome to infocyn Telegram Username Tool!{RESET}\n"
    for char in welcome_msg:
        print(char, end='', flush=True)
        time.sleep(0.003)
    
    # Telegram channel and reminder
    link_msg = f"{YELLOW}Join our channel and stay updated: https://t.me/infocyn{RESET}\n"
    for char in link_msg:
        print(char, end='', flush=True)
        time.sleep(0.003)
    
    # Display fishing hook
    print(HOOK + "\n")

# --------------------- Help Screen ---------------------
def help_screen():
    print(BOLD + "\nInstructions:" + RESET)
    print("""
1) Start username generator — generates rare usernames.
2) Show last results — display recently generated usernames.
3) Help — show this help menu.
4) Exit — close the tool safely.
""")

# --------------------- Username Generator ---------------------
def usernameG():
    y = ''.join(random.choice(string.ascii_lowercase) for _ in range(1))
    j = ''.join(random.choice(string.ascii_lowercase) for _ in range(1))
    w = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(1))
    ls = [
        y+j+y+j+y, y+'_'+j+'_'+w, y+'_'+w+'_'+j, y+j+j+j+w,
        y+j+j+j+j+j+j, y+w+j+j+j, y+y+y+j+j, y+y+'_'+j+y
    ]
    return random.choice(ls)

# --------------------- Fragment Checker ---------------------
def fragment(username):
    headers = {'user-agent': UserAgent().random}
    try:
        response = get(f'https://fragment.com/username/{username}', headers=headers)
        soup = S(response.content, 'html.parser')
        ok = soup.find("meta", property="og:description").get("content")
        if "is taken" in ok: return "is taken"
        elif "Check the current availability of" in ok: return True
        return False
    except:
        return False

# --------------------- Telegram Checker ---------------------
def checker(username, client):
    global COUNT
    try:
        check = client(CheckUsernameRequest(username=username))
        if check:
            print(f'{GREEN}USER TRUE: {username}{RESET}')
            claimed = climed(client, username)
            claim_flag = True if claimed and fragment(username) == "is taken" else False
            telegram_notify(client, claim_flag, username)
        else:
            print(f"{RED}USER Taken: {username}{RESET}")
    except errors.UsernameInvalidError:
        print(f"{RED}Invalid Username: {username}{RESET}")
        open("banned4.txt","a").write(username+'\n')
    except errors.FloodWaitError as timer:
        print(f"{RED}Flood Wait: {timer.seconds} seconds{RESET}")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")

# --------------------- Telegram Notify ---------------------
def telegram_notify(client, claim, username):
    global COUNT
    text = f'''
🎣 [HIT USER BY - infocyn] 🎣
User: @{username}
URL: https://t.me/{username}
Clicks: {COUNT}
BY: @infocyn
'''
    COUNT += 1
    try:
        if claim:
            client.send_file(username, file='https://t.me/fzzof/4', caption=text)
        else:
            client.send_message('me', text)
    except:
        pass

# --------------------- Channel Claimed ---------------------
def climed(client, username):
    try:
        result = client(functions.channels.CreateChannelRequest(
            title=f'{username}', about=f'User by {USERNAME}', megagroup=False))
        client(functions.channels.UpdateUsernameRequest(channel=result.chats[0], username=username))
        return True
    except:
        return False

# --------------------- Client ---------------------
def clientX():
    client = TelegramClient("Client",
                            b64decode("MjUzMjQ1ODE=").decode(),
                            b64decode("MDhmZWVlNWVlYjZmYzBmMzFkNWYyZDIzYmIyYzMxZDA=").decode())
    client.start()
    return client

# --------------------- Start Generation ---------------------
def start_generation(client):
    if not path.exists('banned4.txt'):
        open('banned4.txt','w').close()
    if not path.exists('flood.txt'):
        open('flood.txt','w').close()
    while True:
        username = usernameG()
        with open('banned4.txt', 'r') as file:
            if username in file.read():
                print(f'{RED}USER BANNED: {username}{RESET}')
                continue
        LAST_GENERATED.append(username)
        checker(username, client)

# --------------------- Menu ---------------------
def menu():
    welcome_screen()
    client = clientX()
    while True:
        print("\nMenu Options:")
        print(f"{YELLOW}1){RESET} Start Username Generator")
        print(f"{YELLOW}2){RESET} Show Last Generated")
        print(f"{YELLOW}3){RESET} Help")
        print(f"{YELLOW}4){RESET} Exit")
        choice = input(CYAN + "Select option: " + RESET).strip()
        if choice == "1":
            start_generation(client)
        elif choice == "2":
            for u in LAST_GENERATED[-10:]:
                print(u)
        elif choice == "3":
            help_screen()
        elif choice == "4":
            print(GREEN + "Goodbye!" + RESET)
            sys.exit()
        else:
            print(YELLOW + "Invalid option!" + RESET)

# --------------------- Run ---------------------
if __name__ == "__main__":
    menu()
