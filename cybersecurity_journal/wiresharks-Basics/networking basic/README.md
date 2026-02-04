#  Networking Fundamentals for Cybersecurity (Cisco-Based)

Welcome to my comprehensive guide on Networking Basics, curated through the **Cisco NetAcad Networking Basics** course. This documentation bridges the gap between core network engineering and practical security analysis.

---

##  1. The OSI Architecture: A Security Perspective
Understanding how data moves is the first step in defending it.

| Layer | Protocol Data Unit (PDU) | Key Protocols | Security Focus |
| :--- | :--- | :--- | :--- |
| **L7 - Application** | Data | HTTP, DNS, SSH, FTP | Web Attacks (SQLi, XSS), API Security |
| **L4 - Transport** | Segment | TCP, UDP | Port Scanning, SYN Flooding, Session Hijacking |
| **L3 - Network** | Packet | IP, ICMP, IPSec | IP Spoofing, Routing Attacks, Firewalls |
| **L2 - Data Link** | Frame | ARP, Ethernet | ARP Poisoning, MAC Spoofing, VLAN Hopping |



---

##  2. Transport Layer Deep-Dive: TCP vs UDP

### **The TCP Three-Way Handshake**
TCP is reliable because it "talks" before it sends data.
1. **SYN (Synchronize):** "Let's connect."
2. **SYN-ACK:** "I'm ready, let's go."
3. **ACK (Acknowledge):** "Connection established."



### **Hacker's Insight: Nmap Scanning**
* **TCP Connect Scan (`-sT`):** Completes the full handshake. Highly visible in logs.
* **SYN Stealth Scan (`-sS`):** Sends `SYN`, gets `SYN-ACK`, then sends `RST` (Reset). It "peeks" at the port but never opens a connection to remain stealthy.
* **Filtered State:** When Nmap gets no response, it usually means a **Firewall** is dropping packets (ICMP/TCP).

---

##  3. Addressing & OS Fingerprinting

### **IP Addressing & CIDR**
* **`/32` (Single Host):** Refers to exactly one IP (e.g., `192.168.1.5/32`).
* **`/24` (Subnet):** Standard LAN with 256 addresses (`0-255`).
* **Default Gateway:** The "Exit Door" (Router). Without this, a device cannot reach the Internet.

### **OS Fingerprinting via TTL (Time To Live)**
We can guess the target OS just by analyzing the TTL value in a `ping` response:
* **TTL ~64:** Likely **Linux/Unix/Mac**.
* **TTL ~128:** Likely **Windows**.

---

## 4. Practical Traffic Analysis (Wireshark)

### **Essential Security Filters**
| Goal | Wireshark Filter |
| :--- | :--- |
| Find Plaintext Passwords | `http.request.method == "POST"` |
| Spot ARP Poisoning | `arp.duplicate-address-frame` |
| Filter by Host IP | `ip.addr == 192.168.1.10` |
| Detect SYN Scans | `tcp.flags.syn == 1 && tcp.flags.ack == 0` |
| View Web Content | `http contains "admin"` |

### **Analysis Workflow**
* **Follow Stream:** Right-click a TCP/HTTP packet → **Follow > TCP Stream** to read the full conversation in plain text (if unencrypted).
* **Conversations:** Use `Statistics > Conversations` to identify "Top Talkers" in a network.

---

##  5. Core Services Summary
* **ARP (Port 0 - L2):** Resolves IP to MAC. Vulnerable to **Man-In-The-Middle (MITM)** via ARP Spoofing.
* **DNS (Port 53):** Resolves Hostnames to IPs. 
* **DHCP (DORA):** How devices get IPs automatically: **D**iscover, **O**ffer, **R**equest, **A**cknowledge.
* **NAT:** Allows Private IPs to communicate with the Public Internet.

---

**Author:** Mohammad Riyazuddin
**Focus:** Cybersecurity & Network Research
**Course Reference:** Cisco Networking Academy