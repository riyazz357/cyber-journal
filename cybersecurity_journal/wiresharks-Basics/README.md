# DAY 1
i saw that http websites send the data "as it" written(plain text).
if i use a public wifi, a hacker can use tool like wireshark to read the password easily.
always check for the lock icon before entering the password to any website.

get methods is use to send the data in web address(URL). everyone can see it.
post method is used to hides the data inside the packet "body"
i learned that hackers specifically search for POST packets because that is where passwords and private info are usually hidden.

before sending any real data, a computer must establish a connection.
they do this in 3 steps:

1. SYN: Client says "Can we connect?"

2. SYN-ACK: Server says "Yes, I am ready."

3. ACK: Client says "Okay, connected."

wireshark is an x-ray machine.
wireshark show me the hidden layers of internet
i saw how data is packed: Frame (Hardware) $\rightarrow$ IP (Address) $\rightarrow$ TCP (Port) $\rightarrow$ HTTP (Data).

# DAY 2

The Secure Web (HTTPS & TLS) When I switched to analyzing HTTPS (Port 443), the difference was immediately visible. Unlike the readable text in HTTP, the data appeared as random, unreadable "garbage" or binary symbols. This is Encryption in action, powered by the TLS (Transport Layer Security) protocol. I observed the TLS Handshake, where the browser and server exchange "Client Hello" and "Server Hello" messages to agree on encryption keys and verify the server's identity using a Certificate. In modern versions like TLS 1.3, this handshake is optimized for speed, often encrypting the traffic immediately after the server's first reply, which is why i saw "Application Data" appear so quickly in the packet stream.

Modern Evolution (QUIC) Finally, I noticed that modern tech giants like Google and YouTube often bypass the traditional TCP route entirely. Instead, they use a new protocol called QUIC (HTTP/3), which runs over UDP. In Wireshark, this appears as "Initial" packets rather than the standard TCP handshake. This protocol combines the connection setup and encryption into a single step, making the modern web significantly faster and more efficient than older standards.

# DAY 3

## Active Reconnaissance: 
Mapping the NetworkThe Concept of Ports and NmapToday, I shifted from "Passive Sniffing" (just watching traffic with Wireshark) to "Active Scanning" using a tool called Nmap. I learned to visualize an IP address as a house and Ports as the doors and windows to that house. For example, Port 80 is the door for Web traffic, and Port 22 is for SSH. Nmap acts like a security guard that knocks on every door to see which ones are open and who is inside. This process is the first step in any security assessment because you cannot hack what you cannot find.

## Aggressive Scanning and Fingerprinting : 
I performed an "Aggressive Scan" using the command nmap -A. This scan went beyond just checking if a port was open; it actually interrogated the service to find out exactly what software and version were running (for example, "OpenSSH 6.6" or "Apache Web Server"). I learned that this is called "Fingerprinting." This step is crucial for both hackers and defenders because knowing the exact version number allows a hacker to search for specific vulnerabilities associated with that old software.

## The Stealth Scan 
(The "Half-Open" Technique)Using Wireshark alongside Nmap, I analyzed how a Stealth Scan (nmap -sS) works. I observed that Nmap cheats the standard TCP 3-Way Handshake. Instead of completing the normal connection process (SYN  SYN-ACK  ACK), Nmap sends a SYN packet, receives a SYN-ACK from the server, and then immediately sends a RST (Reset) packet to cancel the connection. By not sending the final "ACK," the connection is never fully established. This makes the scan faster and often allows it to bypass basic server logs that only record completed connections.Building a Scanner with PythonFinally, I moved from using tools to building our own. I wrote a basic Port Scanner using Python's socket library. I learned that a "Socket" is just a software endpoint that establishes a bidirectional communication channel. Our script works by attempting to connect to a range of ports on a target IP. If the connect_ex() function returns a result of 0, it means the connection was successful and the port is "Open." This exercise proved that complex tools like Nmap are essentially just automated scripts running logical connection attempts in the background.

# DAY 4

1. Beyond Scanning: Active Interaction (Netcat) After discovering open ports using Nmap, the next step is to interact with them. I used a tool called Netcat (nc), often called the "Swiss Army Knife" of networking. Unlike Nmap, which just checks if a door is open, Netcat actually walks through the door. In Bandit Level 14, i used the command nc localhost 30000 to establish a direct, raw TCP connection to the server. This allowed us to send data (the password) manually and receive a response, proving that i can communicate with services without needing a web browser or specific software.

2. Handling Encryption (OpenSSL) i learned that Netcat has a limitation: it communicates in plain text. When i tried to connect to Bandit Level 15 on port 30001, i failed because that port was using SSL/TLS encryption (just like HTTPS). To talk to this secure port, i used the OpenSSL tool. The command openssl s_client -connect localhost:30001 performed the necessary "Handshake" to handle encryption, allowing us to send the password safely. This taught us that different ports speak different "languages" (Plain vs. Encrypted), and i need the right tool for each.

3. Banner Grabbing (The Information Leak) Finally, i upgraded our Python Port Scanner to perform "Banner Grabbing." By sending a simple "Hello" message to an open port, I tricked the server into replying with its details. Our script revealed that the target was running "OpenSSH 6.6.1" and "Apache 2.4.7" on an Ubuntu server. This technique is critical for hackers because identifying the exact software version allows them to search for specific vulnerabilities (exploits) associated with that old version, making the server an easy target.


# Day 5: Wireshark Level 1 - Packet Anatomy

##  Overview
Today, I moved beyond just capturing traffic to performing **"Packet Surgery."** I learned that a network packet is like a **Matryoshka Doll** (layers inside layers). To understand network traffic, we must analyze the headers of each layer in Wireshark's "Packet Details" pane.

---

## Layer 2: Ethernet II (The Hardware)
This layer handles local delivery (LAN). It tells us **who** is talking on the physical network.

### 1. MAC Address & OUI
* **Concept:** The first 6 digits of a MAC Address are called the **OUI** (Organizationally Unique Identifier).
* **Usage:** This allows a hacker or analyst to identify the **Manufacturer** of the device (e.g., Apple, Dell, Cisco).
* **Why it matters:** Identifying the hardware helps in mapping the network infrastructure.

---

##  Layer 3: Internet Protocol v4 (The OS & Distance)
This layer handles global delivery. It contains crucial metadata about the source and destination.

### 1. Time To Live (TTL)
* **Concept:** A countdown number that decreases by **1** every time the packet crosses a Router.
* **Math:** `Starting Value` - `Current Value` = `Number of Routers crossed`.
* ** OS Fingerprinting:** We can guess the Operating System based on the initial TTL value:
    * **TTL ~64:** Linux / Android / MacOS
    * **TTL ~128:** Windows
    * **TTL ~255:** Cisco / Network Gear

### 2. IP Flags (Fragmentation)
* **DF (Don't Fragment):** * If `1`: "Do not break me." (Rigid).
    * If `0`: "You can break me if needed." (Flexible).
* **MF (More Fragments):** * If `1`: "I am broken, more pieces are coming."
    * If `0`: "I am complete."

---

##  Layer 4: TCP (The Behavior)
This layer manages the connection rules, speed, and reliability.

### 1. TCP Flags (The Switches)
Flags indicate the state of the conversation:
* **SYN:** "Hello, I want to connect." (Start)
* **ACK:** "I heard you / Connection established." (Reply)
* **RST:** "Reset/Cut the connection immediately." (Error/Block)
* **FIN:** "I am finished, goodbye." (End)

### 2. Window Size (The Speed Limit)
* **Concept:** Think of this as a **Bucket**. It tells the sender how much empty space the receiver has.
* **High Value (e.g., 65535):** "I have lots of space, send data fast!"
* **Zero (0):** "Stop! My buffer is full." (This causes slow internet/lag).

---

## Practical Case Study: My Analysis
I analyzed a live packet from my network and diagnosed the following:

> **Target Packet Findings:**
>
> 1.  **Hardware Identification:** >     * **Observation:** OUI showed "Ruijie Networks".
>     * **Conclusion:** The device is professional networking gear (likely a Switch/Router).
>
> 2.  **OS & Distance:**
>     * **Observation:** TTL was **123**.
>     * **Calculation:** Windows default is 128. `128 - 123 = 5`.
>     * **Conclusion:** The packet came from a **Windows-based system** and traveled through **5 Routers**.
>
> 3.  **Connection Health:**
>     * **Observation:** IP Flags (DF/MF) were **0** (Not Set). Window Size was **1047**.
>     * **Conclusion:** The connection is flexible (fragmentation allowed) but the device has a small buffer (1047 bytes), suggesting it might be an IoT device or a busy router.

---

## Checklist for Future Analysis
When inspecting a packet, always check these 4 points:
- [x] **OUI:** Who made the device?
- [x] **TTL:** What is the OS and how far is it?
- [x] **TCP Flags:** Is it a Start (SYN), Reply (ACK), or Error (RST)?
- [x] **Window Size:** Is the network congested?