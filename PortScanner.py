#!/usr/bin/python3

import argparse
import time
import threading
from socket import *

openPorts = 0
scanThreads = []
runningThreads = 0
lock = threading.Lock()

def scan(host, port):
    global openPorts
    global runningThreads
    runningThreads += 1

    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        lock.acquire()
        openPorts += 1
        print("[+] %d open" % port)
        lock.release()
        s.close()
    except:
        pass
   
    runningThreads -= 1


def main():
    p = argparse.ArgumentParser(description="Port Scanner.")
    p.add_argument("-H", dest="hosts", type=str)
    args = p.parse_args()

    if args.hosts is None:
        print("Usage: PortScaner.py -H 127.0.0.1,192.168.1.1,...")
        return

    hosts = args.hosts.split(",")
    setdefaulttimeout(1)
    for host in hosts:
        print("Scanning the host: %s ..." % (host))
        for port in range(1, 65535):
            while runningThreads > 800:
                time.sleep(0.01)
                
            t = threading.Thread(target=scan, args=(host, port))
            scanThreads.append(t)
            t.start()

        for t in scanThreads:
            t.join()

        print("[*] The host: %s scan is complete!" % (host))
        print("[*] A total of %d open port" % (openPorts))


if __name__ == "__main__":
    main()
