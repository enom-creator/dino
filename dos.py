# script.py
# -*- coding: utf-8 -*-

import requests, time, colorama, socket, urllib3, threading
try:
    import cymruwhois
except Exception as e:
    from subprocess import run
    from subprocess import PIPE
    run(['pip', 'install', 'cymruwhois'])

# Color codes and initialize colorama
from colorama import Fore, Back, Style, init
init()

def attack_multiple(ip, port, useragent, method='GET', query=''):
    headers = {"User-Agent": useragent, "Connection": "close"}

    if method == "GET":
        response = requests.get(url=f"http://{ip}:{port}/{query}", timeout=2, headers=headers, verify=False, pool_maxsize=15, 
                                 pool_prealoc=15)

        if response.status_code not in [200, 202]:
            warning_black("[*] Error connecting to Server : " + str(server))

    elif method == "POST":
        response = requests.post(url=f"http://{ip}:{port}/", timeout=2, data="A", headers=headers, verify=False, pool_maxsize=15, 
                                 pool_prealoc=15)
        if response.status_code not in [200, 202]:
            warning_black("[*] Error connecting to Server : " + str(server))


# Start a series of attacks on the target system (IP or domain), listening ports (1-65535)
def main(ip):
    try:
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((ip, 80))
        website_ip = socket.gethostname()
    except:
        website_ip = ip

    user_agents = [user_agent for user_agent in cymruwhois.get_agentstrings() if user_agent]
    user_agents = user_agents[:32]

    for port in range(1, 65536):
        for user_agent in user_agents:
            attack_multiple(website_ip, port, user_agent)

    return "Completed"


if __name__ == '__main__':
    main(target)

