import os import time import json import sys import random from telethon.sync import TelegramClient from telethon.sessions import StringSession from telethon.tl.functions.channels import InviteToChannelRequest from telethon.errors import FloodWaitError, UserPrivacyRestrictedError, ChatWriteForbiddenError from colorama import Fore, Style, init

init(autoreset=True)

BANNER = f""" {Fore.CYAN}########################################

TG SCRAPER - ADVANCED MODE

######################################## {Style.RESET_ALL} """

SESSION_FILE = "session.txt" CONFIG_FILE = "config.json" MAX_RETRIES = 3 SAFE_DELAY_RANGE = (5, 10)  # Random delay between actions to avoid bans

def print_colored(text, color=Fore.WHITE): print(color + text + Style.RESET_ALL)

def load_config(): if not os.path.exists(CONFIG_FILE): print_colored("[!] Config file not found! Creating default config.json", Fore.YELLOW) default_config = { "source_group": "source_group_id_or_username", "destination_group": "destination_group_id_or_username", "delay": 5, "max_add_per_run": 10, "filter_premium": False } with open(CONFIG_FILE, "w") as f: json.dump(default_config, f, indent=4) sys.exit("Please edit config.json and restart the script.") with open(CONFIG_FILE, "r") as f: return json.load(f)

def add_account(): global client print_colored("[*] Logging into Telegram...", Fore.CYAN) if os.path.exists(SESSION_FILE): with open(SESSION_FILE, "r") as f: session_string = f.read().strip() client = TelegramClient(StringSession(session_string), 1234567, "your_api_hash_here") print_colored("[+] Session loaded successfully!", Fore.GREEN) else: client = TelegramClient(StringSession(), 1234567, "your_api_hash_here") with client: session_string = client.session.save() with open(SESSION_FILE, "w") as f: f.write(session_string) print_colored("[+] Session saved successfully!", Fore.GREEN)

def scrape_members(premium_only=False): config = load_config() source_group = config["source_group"]

async def run():
    await client.start()
    print_colored(f"[*] Scraping members from {source_group}...", Fore.BLUE)
    members = await client.get_participants(source_group)
    if premium_only:
        members = [m for m in members if m.premium]
        print_colored(f"[✓] Filtered premium members: {len(members)}", Fore.MAGENTA)
    else:
        print_colored(f"[✓] Total members scraped: {len(members)}", Fore.GREEN)
    return members

with client:
    return client.loop.run_until_complete(run())

def add_members(): config = load_config() destination_group = config["destination_group"] max_add = config["max_add_per_run"] members = scrape_members()

async def run():
    await client.start()
    count = 0
    for member in members:
        if count >= max_add:
            print_colored("[!] Max members added per run reached. Exiting...", Fore.YELLOW)
            break
        try:
            await client(InviteToChannelRequest(destination_group, [member]))
            print_colored(f"[+] Added: {member.username or member.id}", Fore.GREEN)
            count += 1
            delay = random.randint(*SAFE_DELAY_RANGE)
            print_colored(f"[*] Waiting {delay} seconds before next action...", Fore.BLUE)
            time.sleep(delay)
        except FloodWaitError as e:
            print_colored(f"[!] Telegram FloodWait detected! Waiting {e.seconds} seconds...", Fore.RED)
            time.sleep(e.seconds)
        except UserPrivacyRestrictedError:
            print_colored("[-] Cannot add user due to privacy settings", Fore.YELLOW)
        except ChatWriteForbiddenError:
            print_colored("[-] Bot has no permission to add users!", Fore.RED)
            break
        except Exception as e:
            print_colored(f"[-] Failed to add {member.username or member.id}: {e}", Fore.RED)

with client:
    client.loop.run_until_complete(run())

def main(): while True: os.system("cls" if os.name == "nt" else "clear") print(BANNER) print_colored("\nTG SCRAPER - Select an Option:", Fore.CYAN) print(Fore.YELLOW + "1. Add Telegram Account") print(Fore.YELLOW + "2. Scrape Members") print(Fore.YELLOW + "3. Scrape Premium Members") print(Fore.YELLOW + "4. Add Scraped Members to Group") print(Fore.YELLOW + "5. Exit")

choice = input(Fore.CYAN + "\nEnter your choice: ")
    if choice == "1":
        add_account()
    elif choice == "2":
        scrape_members()
    elif choice == "3":
        scrape_members(premium_only=True)
    elif choice == "4":
        add_members()
    elif choice == "5":
        print_colored("[*] Exiting...", Fore.RED)
        sys.exit()
    else:
        print_colored("[!] Invalid choice! Please try again.", Fore.RED)

if name == "main": main()

