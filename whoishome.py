# === Importing Dependencies === #
import packnet as pnet
from time import time, sleep
from threading import Thread



# === Settings === #
target_file = "targets.txt"
interval = 10
timeout = 3



# === Load Targets Function === #
def load_file(target_file):
    with open(target_file, "r") as f:
        return [ l.upper() for l in f.read().splitlines() ]



# === Target Class === #
class Target(Thread):
    def __init__(self, ip, interval, timeout):
        super().__init__()
        self.daemon = True

        self.interval = interval
        self.timeout = timeout
        self.ip = ip
        self.mac = None
        self.last_seen = None
        self.last = None

        self.start()


    def run(self):
        while True:
            addr = pnet.general.getmac(self.ip, timeout=self.timeout)
            if (addr != None):
                if (self.mac == None):
                    self.mac = str(addr.mac)

                self.last_seen = time()

            if (self.last_seen != None):
                self.last = int( time() - self.last_seen )

            sleep(self.interval)



# === Main === #
targets = [ Target(ip, interval, timeout) for ip in load_file(target_file) ]

while True:
    # Here you can acces each target and do your processing.
    # The targets contain three important attributes.
    #   - ip, to identify target.
    #   - mac, also to identify target. (Default value is None when not available)
    #   - last, last seen in seconds. (Default is None when never seen target)

    for target in targets:
        print( f"\nip: {target.ip}\nmac: {target.mac}\nlast: {target.last}\n" )
    sleep(1)
