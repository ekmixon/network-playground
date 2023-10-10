# A simple TCP port scanner to see if it works;
import socket
import threading
import sys

class BortScanner():
    isHostDown = False

    def __init__(self):
        portsRange = range(0, 1024)
        hosts = self.getHostsToScan()

        for host in hosts:
            self.isHostDown = False
            print("\n\nScanning %s for open ports in the %s" % (host, portsRange))

            for port in portsRange:
                if not self.isHostDown:
                    scanningThread = threading.Thread(target=self.scanPort, args=[host, port])
                    scanningThread.run()
                else: break

    def getHostsToScan(self):
        hosts = []

        if len(sys.argv) > 1:
            hosts = [sys.argv[1]]
        else:
            hosts.extend(f"192.168.2.{str(ip)}" for ip in range(1, 255))
        return hosts

    def scanPort(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(.1)

        try:
            result = s.connect_ex((host, port))
            if result == 0:
                print(f"[!] Open: {str(port)}")
                self.isHostDown = False
            elif result in [113, 11]:
                self.isHostDown = True
                print(f"Host {str(host)} seems to be down..")
            s.close()
        except: pass

scanner = BortScanner()