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




# LAB 2ND

#  Lab: High-level logic vulnerability (PortSwigger)
**Goal:** Purchase the "Lightweight l33t leather jacket" with only $100 of store credit.
**Vulnerability:** Business Logic Flaw (Inadequate validation of quantity/integer ranges).

##  The Concept
The application fails to validate whether the `quantity` parameter sent by the user is a positive integer. By sending a negative quantity for a cheaper item, an attacker can deduct the price of that item from the total cart value. This allows the attacker to offset the cost of an expensive item and bypass the account balance restrictions, provided the final cart total remains greater than $0.

##  Methodology & Steps

### Step 1: Add the Target Item
1. Log in with `wiener:peter`.
2. Add the expensive item (Lightweight l33t leather jacket, $1337.00) to your cart normally.

### Step 2: Intercept and Inject Negative Quantity
1. Navigate to a cheaper item (e.g., Diet Coke).
2. Turn on Intercept in Burp Suite.
3. Click "Add to cart".
4. In the intercepted `POST /cart` request, modify the `quantity` parameter to a negative integer.
   *Example:* `productId=2&redir=PRODUCT&quantity=-75`
5. Forward the request and turn off Intercept.

### Step 3: Balance and Exploit
1. Check your shopping cart.
2. The total cost will now be the price of the jacket MINUS the cost of the negative quantity items.
3. Ensure the **Total is greater than $0.00 but less than your store credit ($100.00)**. 
   *(If the total goes negative, the application will usually reject the checkout. Adjust quantities using Burp Repeater if needed).*
4. Click **"Place order"** to successfully checkout and solve the lab.

---
**Key Takeaway / Mitigation:** Always validate user inputs strictly. For quantities, backend systems must enforce a rule that `quantity > 0` and ensure that integer manipulation (like integer overflows/underflows) cannot cause arithmetic logical bypasses during checkout.