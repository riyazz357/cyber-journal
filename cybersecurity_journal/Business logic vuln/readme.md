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



# 3rd LAB

#  Lab: Inconsistent security controls (PortSwigger)
**Goal:** Access the admin panel and delete the user `carlos`.
**Vulnerability:** Business Logic Flaw (Inconsistent Security Validation / Privilege Escalation).

## The Concept
The application enforces strict security controls (email verification) during the initial user registration process. However, it fails to apply the same level of security to the "Update Email" functionality. Additionally, the system grants administrative privileges automatically to any user with an `@dontwannacry.com` email address. By changing an already verified email to the privileged domain, an attacker can escalate their privileges without needing to verify the new email address.

##  Methodology & Steps

### Step 1: Account Creation & Verification
1. Access the provided "Email client" and copy your temporary `@exploit-server.net` email address.
2. Go to the Lab's Registration page and sign up for a new account using the temporary email.
3. Check the "Email client" inbox, open the registration email, and click the confirmation link to verify the account.

### Step 2: Privilege Escalation (Inconsistent Control)
1. Log in to your newly verified account.
2. Navigate to the "My account" section where the "Update email" form is located.
3. Change your email address to: `anything@dontwannacry.com`
4. Submit the form. Notice that the application updates the email without sending a verification link to the new address.

### Step 3: Exploit
1. Because your account email now matches the internal corporate domain (`@dontwannacry.com`), the system automatically grants you administrative privileges.
2. Click on the newly visible **"Admin panel"** link in the top navigation bar.
3. Find the user `carlos` and click **"Delete"**.
4. The lab is successfully solved.

---
**Key Takeaway / Mitigation:** Security controls must be applied consistently across all related features. If verifying an email address is required during signup, re-verification MUST be required when a user attempts to change their email address, especially if user roles/privileges are tied to the email domain.


# 4th lab

# Lab: Flawed enforcement of business rules (PortSwigger)
**Goal:** Buy the "Lightweight l33t leather jacket" using coupon stacking to reduce the price to $0.
**Vulnerability:** Business Logic Flaw (Flawed Enforcement of Business Rules / Coupon Stacking).

##  The Concept
The application has a business rule that aims to prevent users from applying the same coupon code multiple times. However, the enforcement logic is flawed: it only checks if the *currently* submitted coupon is the exact same as the *previously* submitted coupon. It fails to check the entire history of applied coupons for the session. By alternating between two different valid coupon codes, an attacker can bypass the check and stack discounts infinitely until the cart value drops to zero.

##  Methodology & Steps

### Step 1: Setup
1. Log in to the application with the provided credentials (`wiener:peter`).
2. Add the target item ("Lightweight l33t leather jacket", $1337.00) to your shopping cart.
3. Navigate to the Cart page.

### Step 2: The Alternate Stacking Exploit
1. In the "Coupon code" input field, enter the first coupon: `NEWCUST5` and apply it.
2. The price will decrease.
3. In the same input field, enter the second coupon: `SIGNUP30` and apply it.
4. The price will decrease further.
5. Re-enter the first coupon: `NEWCUST5` and apply it again. It will be accepted because the *last* applied coupon was `SIGNUP30`.

### Step 3: Takedown
1. Continue alternating between `NEWCUST5` and `SIGNUP30` (or use Burp Repeater to send the `POST /cart/coupon` requests alternately to speed up the process).
2. Keep stacking the discounts until the Total price reaches **$0.00**.
3. Click the **"Place order"** button to check out successfully and solve the lab.

---
**Key Takeaway / Mitigation:** Business rules must be enforced comprehensively. To prevent coupon stacking, the backend should maintain a list (array/set) of all coupons applied to the current cart/session. The logic should evaluate: `If (New_Coupon IN Applied_Coupons_List) -> Reject`.


# 5th lab

# Lab: Low-level logic flaw (PortSwigger)
**Goal:** Purchase the "Lightweight l33t leather jacket" with limited funds ($100).
**Vulnerability:** Low-level Logic Flaw (Integer Overflow).

##  The Concept
The application calculates the total cart value by multiplying the item price (in cents) by the quantity. However, it stores this total in a standard 32-bit signed integer format. The maximum value this data type can hold is `2,147,483,647`. If the total cart value exceeds this number, an **Integer Overflow** occurs, and the value wraps around to a massive negative number (`-2,147,483,648`). By exploiting this, an attacker can manipulate the cart total into a negative value and then balance it back to a small positive amount (under their account balance) to purchase expensive items.

##  Methodology & Steps

### Step 1: Intercept the Cart Request
1. Log in with `wiener:peter`.
2. Add the target item ("Lightweight l33t leather jacket") to the cart.
3. Locate the `POST /cart` request in Burp Suite and send it to **Intruder**.

### Step 2: Trigger the Integer Overflow
1. In Intruder (Positions tab), change the `quantity` parameter in the request body to `99` (the max allowed per UI request) and clear all payload markers.
2. Go to the Payloads tab. Set the Payload type to **Null payloads**.
3. Under Payload Options, set "Generate" to **323** payloads.
4. Start the attack to send 323 consecutive requests, adding 31,977 jackets to the cart.
5. Check the cart in your browser. The total value should now be a large negative number.

### Step 3: Balance the Cart and Exploit
1. Manually add more jackets or other items to the cart to bring the negative total closer to zero.
2. Once the negative amount is small enough, add cheaper items (or specific quantities using Burp Repeater) until the final Cart Total is **greater than $0.00 and less than $100.00**.
3. Click **"Place order"** to complete the purchase and solve the lab.

---
**Key Takeaway / Mitigation:** When dealing with financial calculations, backend systems should use data types that can handle extremely large numbers (like 64-bit integers or BigInt). Additionally, the application must perform explicit boundary checking to prevent the cart total from exceeding logical limits or dropping below zero.


# 6th lab

#  Lab: Inconsistent handling of exceptional input (PortSwigger)
**Goal:** Access the admin panel and delete Carlos by exploiting an email string truncation vulnerability.
**Vulnerability:** Business Logic Flaw (Inconsistent Input Handling / Database Truncation).

##  The Concept
Different components of an application (e.g., the registration handler vs. the database) may process exceptionally long inputs differently. In this lab, the database truncates the `email` field to exactly 255 characters. However, the email-sending mechanism processes the entire input. 
By crafting an email address where the 255th character perfectly ends with a privileged domain (`@dontwannacry.com`), followed by an attacker-controlled domain (`.exploit-server.net`), the attacker receives the verification email. Once verified, the database only stores the truncated, privileged domain, granting the attacker Admin rights.

##  Methodology & Steps

### Step 1: Payload Generation
1. Identify the target privileged domain: `@dontwannacry.com` (17 chars).
2. Calculate the padding needed to reach the 255-character database limit: `255 - 17 = 238 chars`.
3. Create a 238-character string (e.g., 238 'A's).
4. Construct the malicious email payload: 
   `[238 'A's]@dontwannacry.com.[YOUR_EXPLOIT_SERVER_DOMAIN]`

### Step 2: Registration and Verification
1. Go to the Lab's registration page.
2. Register a new user using the constructed malicious payload as the email.
3. Navigate to the exploit server's Email Client. Because the email dispatcher processes the full string, the verification email is delivered to your exploit server.
4. Click the verification link to activate the account.

### Step 3: Privilege Escalation & Exploit
1. Log in to the application with the newly registered credentials.
2. During login, the application reads the email from the database, which was truncated at 255 characters, leaving only: `[238 'A's]@dontwannacry.com`.
3. The system recognizes the privileged domain and grants Admin access.
4. Access the **Admin panel** and delete the user `carlos` to solve the lab.

---
**Key Takeaway / Mitigation:** Input validation and length enforcement must be strictly and consistently applied across ALL layers of the application (Frontend, Backend Logic, and Database). The application backend should actively reject inputs that exceed the maximum allowed length rather than relying on the database to silently truncate them.



# 7th lab



#  Lab: Weak isolation on dual-use endpoint (PortSwigger)
**Goal:** Access the `administrator` account by modifying their password, then delete `carlos`.
**Vulnerability:** Business Logic Flaw (Weak Isolation on Dual-Use Endpoint / Parameter Stripping).

##  The Concept
A dual-use endpoint serves multiple roles (e.g., normal users changing their own passwords AND administrators resetting other users' passwords). The application uses the presence or absence of certain parameters (like `current-password`) to determine which logic path to follow. By intercepting a normal password change request and completely removing the `current-password` parameter, a regular user can trick the backend into executing the administrator-only code path, thereby resetting any user's password without knowing their current one.

##  Methodology & Steps

### Step 1: Intercept Password Change
1. Log in with the provided credentials (`wiener:peter`).
2. Navigate to the password change functionality.
3. Fill out the form: Current password (`peter`), and a new password (`hacker123`).
4. Turn on Intercept in Burp Suite and submit the form.

### Step 2: Parameter Stripping & Target Modification
1. In the intercepted `POST` request, locate the request body containing the parameters.
   *Original:* `username=wiener&current-password=peter&new-password=hacker123&new-password-confirmation=hacker123`
2. Change the `username` parameter to your target: `username=administrator`.
3. **Delete** the entire `current-password` parameter and its value from the request.
   *Modified:* `username=administrator&new-password=hacker123&new-password-confirmation=hacker123`
4. Forward the request and turn off Intercept.

### Step 3: Privilege Escalation & Exploit
1. Log out of your current session.
2. Log in using the hijacked credentials: `administrator` / `hacker123`.
3. Access the newly available **Admin panel**.
4. Delete the user `carlos` to solve the lab.

---
**Key Takeaway / Mitigation:** Never use the exact same endpoint for normal user actions and administrative actions without strictly validating the session's privilege level. The backend MUST explicitly check the user's role (e.g., `if user.role != ADMIN`) before allowing them to bypass validations like providing a current password.

# 8th lab

#  Lab: Insufficient workflow validation (PortSwigger)
**Goal:** Purchase the "Lightweight l33t leather jacket" without sufficient store credit.
**Vulnerability:** Business Logic Flaw (Insufficient Workflow Validation / State Machine Bypass).

##  The Concept
The application's checkout process relies on a multi-step workflow (e.g., Cart -> Payment -> Order Confirmation). The developer assumed that users will only reach the "Order Confirmation" endpoint if they have successfully passed the "Payment" endpoint. Because the application fails to validate the workflow state at the final step, an attacker can simply add an expensive item to their cart and forcefully navigate to the confirmation URL, completely bypassing the payment and balance check mechanism.

##  Methodology & Steps

### Step 1: Reconnaissance (Identify the target endpoint)
1. Log in with the provided credentials (`wiener:peter`).
2. Add a cheap item (e.g., Diet Coke) to your cart.
3. Complete the checkout process normally by clicking "Place order".
4. Observe the URL of the final order confirmation page:
   `GET /cart/order-confirmation?order-confirmed=true`
5. Copy this URL path.

### Step 2: Setup the Target
1. Go back to the home page and add the "Lightweight l33t leather jacket" ($1337) to your cart.
2. Navigate to your Cart. Do NOT click "Place order", as the server will check your balance and reject the request.

### Step 3: Workflow Bypass (The Exploit)
1. While on the cart page, manually edit the URL in your browser's address bar.
2. Append the confirmation path to the lab's base URL:
   `https://<YOUR-LAB-ID>.web-security-academy.net/cart/order-confirmation?order-confirmed=true`
3. Hit Enter.
4. The server blindly processes the confirmation endpoint, assumes payment was completed, and places the order for the jacket, solving the lab.

---
**Key Takeaway / Mitigation:** Never assume a user has completed previous steps in a workflow just because they request a subsequent endpoint. The backend must enforce a strict "State Machine". When the order confirmation endpoint is hit, the server must verify a session-linked token or database flag that explicitly proves `payment_status == SUCCESS` for the current cart.


# 9th lab

#  Lab: Authentication bypass via flawed state machine (PortSwigger)
**Goal:** Bypass the role selection process to gain administrative privileges and delete the user `carlos`.
**Vulnerability:** Business Logic Flaw (Flawed State Machine / Insecure Default State).

##  The Concept
The application's login process involves a multi-stage state machine: Authentication (`POST /login`) followed by Role Selection (`GET /role-selector`). However, the developer made a flawed assumption: if a user bypasses the role selection phase, their session defaults to an `Administrator` role instead of a lower-privileged state (Failing Open). By intercepting and dropping the role-selection request, an attacker can inherit these default high privileges.

##  Methodology & Steps

### Step 1: Intercept the Login Process
1. Turn on Intercept in Burp Suite.
2. Submit the login credentials (`wiener:peter`).

### Step 2: Drop the Role Selector Request
1. In Burp Suite, observe the first request (`POST /login`) and click **Forward**.
2. The server responds with a redirect, and the browser immediately sends the next request: `GET /role-selector`.
3. Instead of forwarding this request, click the **Drop** button to destroy the request completely.
4. Turn off Intercept.

### Step 3: Exploit the Default State
1. In your browser, manually navigate to the homepage or the `/admin` path.
2. Observe that you now have administrative privileges because the state machine failed open.
3. Access the Admin panel and click **Delete** next to the user `carlos` to solve the lab.

---
**Key Takeaway / Mitigation:** State machines must always fail securely ("Fail Closed"). If a user does not explicitly complete the required steps to establish their role, their session should be granted zero privileges or the lowest possible privileges by default. Never assign administrative roles as a fallback default.

# 10th lab

#  Lab: Infinite money logic flaw (PortSwigger)
**Goal:** Exploit a logic flaw to generate enough store credit to buy the "Lightweight l33t leather jacket".
**Vulnerability:** Business Logic Flaw (Arbitrage / Flawed Discount Implementation).

##  The Concept
The application allows users to apply a 30% discount coupon (`SIGNUP30`) to all items in the store, **including gift cards**. Since a gift card represents a fixed monetary value ($10) but can be purchased for less ($7), an attacker can create an infinite money loop. By repeatedly buying discounted gift cards and redeeming them back into their own account, the attacker nets a $3 profit per transaction, eventually generating infinite store credit.

##  Methodology & Steps

### Step 1: The Manual Exploit Loop
1. Log in using `wiener:peter`.
2. Add a $10 Gift Card to your cart.
3. Navigate to the cart and apply the coupon code `SIGNUP30`. The price drops to $7.
4. Click "Place order".
5. On the order confirmation page, copy the generated Gift Card code.
6. Navigate to "My account", paste the code into the Gift Card redemption box, and click "Redeem".
7. Observe that your balance has increased by a net of $3.

### Step 2: Automation via Burp Suite Macros
*(Note: Doing this manually ~400 times is impractical).*
1. Go to **Project Options -> Sessions** in Burp Suite.
2. Create a new **Macro** that records the exact sequence of actions:
   - `POST /cart` (Add to cart)
   - `POST /cart/coupon` (Apply SIGNUP30)
   - `POST /cart/checkout` (Place order)
   - `GET /cart/order-confirmation` (Get the code)
   - `POST /gift-card` (Redeem the code)
3. Set a custom parameter rule to extract the gift card code from the response of the `GET /cart/order-confirmation` request and pass it to the `POST /gift-card` request.
4. Send the final request to Burp Intruder, set null payloads to run 400+ times, and execute the attack.

### Step 3: Purchase the Target Item
1. Once your store credit exceeds $1337, navigate to the target item.
2. Add the "Lightweight l33t leather jacket" to your cart and place the order.

---
**Key Takeaway / Mitigation:** Never treat cash equivalents (like gift cards, wallet top-ups, or digital currency) as regular retail products. Discount codes, promotional offers, and coupons must have strict exclusion rules explicitly preventing them from being applied to monetary or cash-equivalent items.