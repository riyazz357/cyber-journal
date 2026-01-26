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