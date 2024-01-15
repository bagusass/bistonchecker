#!/usr/bin/env python3

import os
import psutil
import json
import argparse
import requests
from threading import Lock
from time import time, gmtime, strftime
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime
from rich.progress import Progress, BarColumn
from pyfiglet import Figlet
from ipscoop import IpScoop

def parse_args():
    parser = argparse.ArgumentParser(description="ProxyTool")
    parser.add_argument('-i', '--input', type=str, help="Input file (proxy list)", required=True)
    parser.add_argument('-t', '--threads', type=int, help="Threads", default=500)
    parser.add_argument('-o', help='file', default='proxy-working.json', type=str)
    parser.add_argument('--show', action='store_true', help="Show live proxies")
    parser.add_argument('--filter', default=False, action='store_true', help='filter by country')
    parser.add_argument('--move', default=False, action='store_true', help='move result filter to outputfolder')
    return parser.parse_args()

class botcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKDARKCYAN = '\033[36m'
    OKGREEN = '\033[92m'
    OKPURPLE = '\033[95m'
    OKLIGHTYELLOW = '\033[33m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    OKBLUEHD = '\033[0;94m'
    OKBLUEBHD = '\033[1;94m'
    UNDERLINE = '\033[4m'

socks5, socks4, http, dead_proxies = 0, 0, 0, 0
protocol = ""

def open_file():
    global protocol
    with open('biston-checker-result.txt', 'r') as f:
        protocol = f.readline().strip().split("://")[0]
        data = f.readlines()
        for proxy in data:
            all_data.append(proxy.strip())
    return data, protocol

def save(line, file):
    lock.acquire()
    with open(file, "w+") as f:
        f.write(line + "\n")
    lock.release()

def save2(data):
    with open(args.o, 'w') as f:
        json.dump(data, f, indent=4)
    
def read_proxy_list(file_path):
    with open(file_path, "r") as f:
        proxylist = f.read().splitlines()
    duplicate_lines_count = len(proxylist) - len(set(proxylist))
    proxylist = list(set(proxylist))
    return proxylist, duplicate_lines_count

def get_system_info():
    cpu_cores = psutil.cpu_count()
    memory_info = psutil.virtual_memory()
    total_memory = memory_info.total / (1024.0 ** 3)
    return {
        'CPU cores': cpu_cores,
        'Total memory': f'{total_memory:.2f} GB',
    }

def check(proxy):
    if '://' in proxy:
        provided_protocol, proxy = proxy.split('://')
    else:
        provided_protocol = None

    for protocol in ["socks5"]: # another option examples ["socks5", "socks4", "http"]
        if provided_protocol and protocol != provided_protocol:
            continue

        try:
            proxies = {
                "http": "{}://{}".format(protocol, proxy),
                "https": "{}://{}".format(protocol, proxy)
            }
            r = requests.post("https://httpbin.org/ip", proxies=proxies, timeout=10)
            if args.show:
                print(f"[{botcolors.WARNING}{protocol.upper()}{botcolors.ENDC}] [{botcolors.OKGREEN}LIVE{botcolors.ENDC}] {proxy}")
            globals()[protocol] += 1
            live_proxies.append(f"{protocol}://{proxy}")
            progress.update(task, advance=1)
            return
        except Exception:
            continue

    if args.show:
        print(f"[{botcolors.FAIL}DEAD{botcolors.ENDC}] {proxy}")
    global dead_proxies
    dead_proxies += 1
    progress.update(task, advance=1)
    
def check_negara(data):
    for proxy in data:
        ip = proxy.split('/')[2].split(':')[0]
        json_data = ip_scoop.data(ip)
        if json_data:
            if json_data.country not in proxies_country:
                proxies_country[json_data.country] = []
            proxies_country[json_data.country].append(proxy)
        else:
            proxies_country['unknown'].append(proxy)

def main():
    global lock, args, progress, task
    os.system('cls' if os.name == 'nt' else 'clear')    
    print(botcolors.OKCYAN + Figlet(font='slant').renderText('BistonChecker') + botcolors.ENDC)

    args = parse_args()
    proxylist, duplicate_lines_count = read_proxy_list(args.input)
    data, protocol = open_file()
    start_message = f"[{botcolors.OKCYAN}*{botcolors.ENDC}] Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} >> [{botcolors.WARNING}Total proxies: {len(proxylist)}{botcolors.ENDC}]"
    
    lock = Lock()
    start_time = time()
    pool = ThreadPool(processes=args.threads)
    progress = Progress("[progress.description]{task.description}", 
                        BarColumn(bar_width=None), 
                        "[progress.percentage]{task.percentage:>3.0f}%", "[progress.bar]{task.completed}/{task.total}")
    task = progress.add_task("[cyan]Live Checking...", total=len(proxylist))
    with progress:
        for _ in pool.imap_unordered(func=check, iterable=proxylist):
            pass
        pool.close()
        pool.join()
    save('\n'.join(live_proxies), "biston-checker-result.txt")
    if dead_proxies > len(live_proxies):
        decrease = ((dead_proxies - len(live_proxies)) / dead_proxies) * 100
        decrease_str = f"(-{decrease:.2f}%)"
    else:
        decrease_str = ""
    t = strftime("%H:%M:%S", gmtime(time() - start_time))
    print("")
    print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] -------------------------  STATS  -------------------------")
    print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] {botcolors.OKCYAN}System Info:{botcolors.ENDC} {botcolors.OKPURPLE}{get_system_info()}{botcolors.ENDC}")
    print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] ")
    print(start_message)
    print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] Checking time: {t}")
    print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] Speed: {round(len(proxylist) / (time() - start_time), 2)} proxies/s")
    if protocol == "socks5":
        print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] SOCKS5: {len(live_proxies)}")
    elif protocol == "socks4":
        print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] SOCKS4: {len(live_proxies)}")
    elif protocol == "http":
        print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] HTTP: {len(live_proxies)}")
    else:
        print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] SOCKS5: {socks5}")
        print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] SOCKS4: {socks4}")
        print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] HTTP: {http}")
    print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] Duplicate proxies : {duplicate_lines_count}")
    print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] save to biston-checker-result.txt")
    print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} >> [{botcolors.OKGREEN}Live: {len(live_proxies)}{botcolors.ENDC}][{botcolors.FAIL}Down: {dead_proxies}{botcolors.ENDC}]{botcolors.OKLIGHTYELLOW}{decrease_str}{botcolors.ENDC}")
    print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] ")

    if args.filter:
        start_time = time()
        open_file()
        print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] {botcolors.OKCYAN}Filter By Country Yes!...{botcolors.ENDC}")
        check_negara(all_data)
        print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] Filter By Country: {len(proxies_country):,} Country")
        print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] Country List: {botcolors.OKDARKCYAN}{list(proxies_country.keys())}{botcolors.ENDC}")
        if len(proxies_country) > 0:
            save2(proxies_country)
            print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] Saved to {args.o}")
        end_time = time() - start_time
        print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] " + f'Total RunTime Filter: {strftime("%H:%M:%S", gmtime(end_time))}')

        if args.move:
            print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] ")
            print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] {botcolors.OKCYAN}Split Export to output_folder Yes!...{botcolors.ENDC}")
            with open(args.o, 'r') as f:
                datajson = json.load(f)
            for country, proxies in datajson.items():
                file_name = os.path.join(output_folder, f'{country.lower()}.txt')
                with open(file_name, 'w') as f:
                    for proxy in proxies:
                        f.write(proxy + '\n')
                print(f"[{botcolors.OKCYAN}*{botcolors.ENDC}] Total proxies for {botcolors.OKDARKCYAN}{country} : {len(proxies)}{botcolors.ENDC} --> save to {file_name} done!")

if __name__ == '__main__':
    ip_scoop = IpScoop('ipscoop.mmdb')
    all_data = []
    proxies_country = {'unknown': []}
    live_proxies = []
    output_folder = 'var/www/html/'
    os.makedirs(output_folder, exist_ok=True)
    main()