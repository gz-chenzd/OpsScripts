import os
import argparse
import httplib2
import threading
import dns.resolver

detectThreads = []
runningThreads = 0

def detect(domain, host, port=80, path="/"):
    global runningThreads
    runningThreads += 1
		
    print("Detecting the host: %s:%d ..." % (host, port))
	
    rspcontent = ""
    destEndpoint = host + ":" + str(port)
    # httplib2.socket.setdefaulttimeout(5)
    conn = httplib2.HTTPConnectionWithTimeout(destEndpoint, timeout=5)
  
    try:
        conn.request("GET", path, headers = {"host": domain})
        response = conn.getresponse() 
        rspcontent = response.read(50)
        print("[+] %s:%d: %s" % (host, port, rspcontent))
    except:
        print("[-] %s:%d: ERROR" % (host, port))

    runningThreads -= 1


def main():
    p = argparse.ArgumentParser(description="Site Reachable Detector.")
    p.add_argument("-D", dest="domain", type=str)
    p.add_argument("-H", dest="hosts", type=str)
    p.add_argument("-P", dest="port", type=int)
    p.add_argument("-p", dest="path", type=str)
    args = p.parse_args()

    hosts = []
    port = 80
    path = "/"

    if args.domain is None:
        print("Usage: SiteDetector.py -D www.site.com")
        return

    if args.hosts and args.hosts.strip():
        hosts = args.hosts.split(",")

    if args.port and args.port > 0:
        port = args.port

    if args.path and args.path.strip():
        path = args.path

    if len(hosts) == 0:
        result = dns.resolver.query(args.domain)
        for i in result.response.answer:
            for j in i.items:
                hosts.append(j.address)
		
    for host in hosts:
        while runningThreads > 10:
            time.sleep(0.01)
                
        t = threading.Thread(target=detect, args=(args.domain, host, port, path))
        detectThreads.append(t)
        t.start()

    for t in detectThreads:
        t.join()

    print("[*] The domain: %s detect is complete!" % (args.domain))


if __name__ == "__main__":
    main()
