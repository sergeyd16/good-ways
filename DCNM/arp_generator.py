from scapy.all import *
import time

SELF_MAC = 'a0:8c:fd:c5:e3:79'    # fill in with your MAC address
BCAST_MAC = 'ff:ff:ff:ff:ff:ff'

def create_ARP_request_gratuituous(ipaddr_to_broadcast):
    arp = ARP(psrc=ipaddr_to_broadcast,
              hwsrc=SELF_MAC,
              pdst=ipaddr_to_broadcast)
    return Ether(src=SELF_MAC, dst=BCAST_MAC) / arp

sendp(create_ARP_request_gratuituous('10.10.10.50'), iface='Ethernet 8')
time.sleep(20)
SELF_MAC = 'a0:8c:fd:c5:e3:79'
sendp(create_ARP_request_gratuituous('10.10.10.50'), iface='Ethernet 8')