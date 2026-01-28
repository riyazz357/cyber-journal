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