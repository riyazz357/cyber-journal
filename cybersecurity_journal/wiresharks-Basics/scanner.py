import socket
import sys
from datetime import datetime

# Target define karo
target = "scanme.nmap.org"

print("-" * 50)
print(f"Scanning Target: {target}")
print(f"Time started: {str(datetime.now())}")
print("-" * 50)

try:
    for port in range(20, 85):
        # Socket object banao (IPv4, TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Timeout set karo 
        s.settimeout(1)
        
     
        result = s.connect_ex((target, port))
        
        if result == 0:
            print(f"Port {port}: OPEN")
            try:
                s.send(b"Hello\r\n")
                banner = s.recv(1024) # 1024 bytes receive karo
                print(f"   Service: {banner.decode().strip()}")
            except:
                print("   Service: Unknown")
        s.close()

except KeyboardInterrupt:
    print("\nExiting program.")
    sys.exit()

except socket.error:
    print("Could not connect to server.")
    sys.exit()