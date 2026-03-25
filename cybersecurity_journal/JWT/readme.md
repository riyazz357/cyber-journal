# 1st lab

#  Lab: JWT authentication bypass via unverified signature
**Platform:** PortSwigger Web Security Academy
**Goal:** Modify the JWT session cookie to access the admin panel and delete user `carlos`.
**Vulnerability:** Insecure JWT Implementation (The server decodes the payload but completely fails to verify the signature cryptographically).

##  Prerequisites (The Pro Tool)
To avoid manual Base64URL encoding errors (like padding `=` or accidental spaces), use the **JWT Editor** extension.
1. In Burp Suite, go to **Extensions -> BApp Store**.
2. Search for **JWT Editor** and click **Install**.

[Image of Burp Suite JWT Editor extension modifying payload claims]

## Step-by-Step Exploitation

### Step 1: Capture the Session Token
1. Log in to the application using the given credentials (`wiener:peter`).
2. Go to Burp Suite's **HTTP History** and find the `GET /my-account` request.
3. Right-click the request and select **Send to Repeater (Ctrl+R)**.

### Step 2: Forge the JWT Payload
1. Go to the **Repeater** tab.
2. On the right side panel (Inspector/Message Editor), look for the newly added **JSON Web Token** tab.
3. Expand the **Payload** section. You will see the user claims, including `"sub": "wiener"`.
4. Change the value of `"sub"` to `"administrator"`.
5. **Crucial:** Click the **Apply changes** button at the bottom of the JWT panel. Burp will automatically re-encode the payload safely into the `Cookie` header without messing up the formatting or signature.

### Step 3: The Takedown (Access Admin & Delete)
1. In the same Repeater request, change the top request line from `GET /my-account HTTP/2` to **`GET /admin HTTP/2`**.
2. Click **Send**. You should get a `200 OK` response, confirming you are now an Admin.
3. To finish the lab, change the request line again to **`GET /admin/delete?username=carlos HTTP/2`**.
4. Click **Send**. The lab will be marked as solved! 

---
**Key Takeaway:** Never trust client-provided data. Even if a JWT looks valid, the backend MUST verify the signature using the server's secret key before trusting the claims inside the payload.


# 2nd lab

#  Lab: JWT authentication bypass via flawed signature verification
**Platform:** PortSwigger Web Security Academy
**Goal:** Modify the JWT session cookie to access the admin panel and delete user `carlos`.
**Vulnerability:** Insecure JWT Implementation (The server blindly trusts the `alg` header provided by the client, allowing the `none` algorithm to bypass signature verification).

##  The Concept (The `alg: none` Attack)
The JWT specification originally included a `none` algorithm intended for debugging purposes, meaning the token has no signature. A critical vulnerability occurs if a backend server dynamically selects its signature verification algorithm based purely on the `alg` parameter present in the JWT Header. 
An attacker can manipulate the Header to `"alg": "none"`, elevate privileges in the Payload (e.g., `"sub": "administrator"`), and completely remove the Signature (leaving only the trailing dot `.`). The server reads `alg: none`, skips signature verification, and accepts the forged token.

##  Prerequisites
* Burp Suite with the **JWT Editor** extension installed (via BApp Store).

##  Step-by-Step Exploitation

### Step 1: Capture the Target Token
1. Log in to the application using standard credentials (`wiener:peter`).
2. Go to Burp Suite's **HTTP History** and find the `GET /my-account` request.
3. Send this request to **Repeater (Ctrl+R)**.

### Step 2: Forge the Token via JWT Editor
1. In the Repeater tab, click on the **JSON Web Tokens** extension tab.
2. Under the **Payload** section, locate the user claim: `"sub": "wiener"`.
3. Change it to the target user: `"sub": "administrator"`.
4. Click the **Attack** button at the bottom and select **None Signing Algorithm**.
5. Click **OK** on the prompt to update headers. 
   *(Note: The extension automatically changes the header to `"alg": "none"` and strips the signature, leaving the required trailing dot `.`).*

### Step 3: Privilege Escalation & Takedown
1. Switch back to the raw **Request** tab in Repeater. Verify that the `session` cookie now ends with a single dot (e.g., `eyJ... .eyJ... .`).
2. Modify the first line of the HTTP request from `GET /my-account HTTP/2` to **`GET /admin HTTP/2`**.
3. Click **Send**. You should receive a `200 OK` response.
4. Modify the request line again to **`GET /admin/delete?username=carlos HTTP/2`** and click **Send**.
5. The lab is successfully solved! 

---
**Key Takeaway / Mitigation:** Never trust the client-supplied `alg` header. The server must enforce a strict, hardcoded whitelist of allowed algorithms (e.g., only `HS256` or `RS256`) and explicitly reject any tokens specifying `none` in a production environment.


# 3rd LAB

