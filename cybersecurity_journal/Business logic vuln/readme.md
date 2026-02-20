# LAB 1

#  Lab: Excessive trust in client-side controls (PortSwigger)
**Goal:** Purchase the "Lightweight l33t leather jacket" with limited store credit.
**Vulnerability:** Business Logic Flaw (Unvalidated Client-Side Input).

##  The Concept
The application relies on the client (browser) to transmit the price of an item when adding it to the shopping cart. Because HTTP requests can be easily intercepted and modified using a proxy (like Burp Suite), an attacker can change the price parameter to any arbitrary value before it reaches the server. The server blindly trusts this modified input without cross-referencing its own database.

##  Methodology & Steps

### Step 1: Recon & Setup
1. Log in to the application using provided credentials (`wiener:peter`).
2. Locate the target item (Lightweight l33t leather jacket) which costs $1337.00.

### Step 2: Intercept and Modify
1. Turn on Intercept in Burp Suite.
2. Click **"Add to cart"** on the product page.
3. In Burp Suite, locate the `POST /cart` request.
4. Look at the request body (the last line). You will see parameters like: 
   `productId=1&redir=PRODUCT&quantity=1&price=133700`
5. Modify the `price` parameter to a minimal value, for example: `price=1` (which equals $0.01).
6. Forward the modified request and turn off Intercept.

### Step 3: Exploit Execution
1. Go to your shopping cart in the browser.
2. Verify that the jacket is now in your cart for $0.01.
3. Click **"Place order"** to successfully purchase the item and solve the lab.

---
**Key Takeaway / Mitigation:** Never pass sensitive data (like prices, discount rates, or user roles) via client-side controls (hidden form fields, cookies, or URL parameters). The server must always look up authoritative data from its own secure backend database using only a non-manipulable identifier (like a `productId`).