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

#  Lab: JWT authentication bypass via weak signing key
**Platform:** PortSwigger Web Security Academy
**Goal:** Crack the JWT secret key, forge a valid admin token, and delete user `carlos`.
**Vulnerability:** Insecure JWT Implementation (The server uses a weak, easily guessable secret key to sign the JWTs using the HS256 symmetric algorithm).

##  The Concept (Offline Dictionary Attack)
When a JWT uses a symmetric algorithm like HS256, the exact same secret key is used to both create the signature and verify it. If a developer uses a weak password as the secret key (like `secret1`, `password`, etc.), an attacker can capture a single valid JWT and run an offline dictionary attack against it. 

The attacker's tool will try hashing the token's header and payload with every password in a wordlist until the resulting signature matches the signature on the captured token. Once the secret key is cracked, the attacker can create new tokens with elevated privileges (e.g., `"sub": "administrator"`) and sign them perfectly using the stolen key. The server will trust the forged token completely.

##  Prerequisites
* A captured JWT from the target application.
* A wordlist of common passwords/secrets (provided in the lab description).
* An offline cracking tool like **Hashcat** (or a custom Python script) OR the Burp Suite **JWT Editor** extension (if setting the key manually).

##  Step-by-Step Exploitation

### Step 1: Capture the Token & Wordlist
1. Log in to the application using standard credentials (`wiener:peter`).
2. Go to Burp Suite's HTTP History, find the `GET /my-account` request, and copy the JWT from the `session` cookie.
3. Download the "wordlist of common secrets" provided on the lab's main page.

### Step 2: Crack the Secret Key (Offline)
*Using Hashcat (Linux/Windows):*
Save the JWT to a file named `jwt.txt` and the wordlist to `wordlist.txt`. Run the following command in your terminal:
`hashcat -a 0 -m 16500 jwt.txt wordlist.txt`
*Result:* Hashcat will crack the token and reveal the weak secret key (usually `secret1`).

### Step 3: Forge the Admin Token
1. Go to [jwt.io](https://jwt.io/) in your browser.
2. Paste your captured JWT into the "Encoded" panel on the left.
3. In the "Decoded" panel on the right, modify the **Payload**: change `"sub": "wiener"` to `"sub": "administrator"`.
4. Scroll down to the **Verify Signature** section. Replace the placeholder `your-256-bit-secret` with your cracked key (`secret1`).
5. Copy the newly generated, properly signed JWT from the left panel.

### Step 4: Privilege Escalation & Takedown
1. Send the `GET /my-account` request to Burp Suite Repeater.
2. Replace your old `session` cookie with the newly forged JWT.
3. Change the request path to `GET /admin HTTP/2` and click **Send** to verify admin access (you should see a `200 OK`).
4. Change the path to `GET /admin/delete?username=carlos HTTP/2` and click **Send**.
5. The lab is successfully solved! 🎉

---
**Key Takeaway / Mitigation:** Always use strong, unpredictable, and cryptographically secure secrets for signing JWTs. A good secret for HS256 should be randomly generated and at least 256 bits (32 bytes) long to prevent offline brute-force attacks.


# 4TH LAB

# Lab: JWT authentication bypass via jwk header injection
**Platform:** PortSwigger Web Security Academy
**Goal:** Forge a JWT using your own RSA key pair, inject the public key via the `jwk` header, bypass authentication, and delete user `carlos`.
**Vulnerability:** Insecure JWT Implementation (The server blindly trusts the `jwk` parameter in the JWT header, dynamically using the attacker's public key to verify the token's signature).

## The Concept (The "Bring Your Own Lock" Attack)
The JSON Web Signature (JWS) specification allows developers to embed their Public Key directly inside the token's header using the `jwk` (JSON Web Key) parameter. 
If the backend server is misconfigured to trust this dynamically provided key instead of using its own statically configured trusted Public Key, an attacker can completely bypass the signature verification process. The attacker simply generates a new RSA key pair, alters the token's payload to elevate privileges (e.g., `"sub": "administrator"`), signs the token with their forged Private Key, and embeds the corresponding forged Public Key in the `jwk` header. The server verifies the token using the attacker's public key, resulting in a successful validation.

##  Prerequisites
* Burp Suite with the **JWT Editor** extension installed.

##  Step-by-Step Exploitation

### Step 1: Generate a Rogue RSA Key Pair
1. In Burp Suite, navigate to the **JWT Editor Keys** tab.
2. Click **New RSA Key**.
3. In the dialog box, click **Generate** to create a new key pair, then click **OK** to save it.

### Step 2: Capture the Target Token
1. Log in to the application using standard credentials (`wiener:peter`).
2. Go to Burp Suite's HTTP History, find the `GET /my-account` request, and send it to **Repeater (Ctrl+R)**.

### Step 3: Forge the Token & Inject JWK
1. In the Repeater tab, switch to the **JSON Web Tokens** extension tab.
2. In the **Payload** section, change the user claim from `"sub": "wiener"` to `"sub": "administrator"`.
3. At the bottom of the tab, click the **Attack** button and select **Embedded JWK**.
4. A prompt will appear asking you to select a key. Choose the RSA key you generated in Step 1 and click **OK**.
   *(Note: The JWT Editor will automatically update the payload, inject your public key into the `jwk` header, and sign the token with your private key).*

### Step 4: Privilege Escalation & Takedown
1. Switch back to the raw **Request** tab in Repeater.
2. Modify the request line to `GET /admin HTTP/2` and click **Send**. You should receive a `200 OK` response, confirming admin access.
3. Modify the request line to `GET /admin/delete?username=carlos HTTP/2` and click **Send**.
4. The lab is successfully solved! 

---
**Key Takeaway / Mitigation:** Never trust cryptographic keys provided by the client in the JWT header (`jwk`, `jku`, `x5c`, etc.). Servers must explicitly enforce signature verification using a pre-configured, trusted public key stored securely on the backend.


# 5TH LAB

#  Lab: JWT authentication bypass via jku header injection
**Platform:** PortSwigger Web Security Academy
**Goal:** Host a malicious JWK on the exploit server, inject the `jku` header to point to it, bypass authentication, and delete user `carlos`.
**Vulnerability:** Insecure JWT Implementation (The server supports the `jku` header and fails to validate whether the provided URL belongs to a trusted domain, allowing SSRF-like behavior to fetch attacker-controlled public keys).

##  The Concept (The "Fake Map" Attack)
The `jku` (JWK Set URL) header specifies a URI where the server can fetch the JSON Web Key (JWK) Set containing the public key needed to verify the token's signature. 
If a server dynamically fetches the public key from the URL provided in the `jku` header without checking if the URL is whitelisted, an attacker can exploit this. The attacker generates an RSA key pair, hosts the Public Key on their own server, modifies the JWT payload (`"sub": "administrator"`), and injects their server's URL into the `jku` header. The target server fetches the attacker's public key, uses it to verify the attacker's forged signature, and grants unauthorized access.

##  Prerequisites
* Burp Suite with the **JWT Editor** extension installed.
* An attacker-controlled server (Exploit Server provided by the lab).

##  Step-by-Step Exploitation

### Step 1: Generate & Copy the Public Key
1. In Burp Suite, go to the **JWT Editor Keys** tab.
2. Click **New RSA Key** -> **Generate** -> **OK**.
3. Right-click the newly created key and select **Copy Public Key as JWK**.

### Step 2: Host the Malicious Key Set
1. Go to the lab's **Exploit Server**.
2. In the **Body** section, create a JSON object with a `keys` array and paste your JWK inside:
   ```json
   {
       "keys": [
           {
               "kty": "RSA",
               "e": "AQAB",
               "kid": "893d8f...", 
               "n": "..."
           }
       ]
   }
   ```
3. Click Store to host this file. Copy the Exploit Server's URL.

### Step 3: Forge the Token & Inject jku
1. Intercept or find the GET /my-account request in Burp and send it to Repeater.

2. Go to the JSON Web Tokens tab.

3. In the Header, update the "kid" to match the ID from your hosted JWK. Add the "jku" parameter pointing to your exploit server:
```
JSON
{
    "kid": "893d8f...",
    "jku": "[https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/exploit](https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/exploit)",
    "alg": "RS256"
}
```
4. In the Payload, change "sub": "wiener" to "sub": "administrator".

5. Click the Sign button at the bottom.

6. Select your RSA key, check the box for "Don't modify header" (Crucial!), and click OK.

### Step 4: Privilege Escalation & Takedown
1. Switch to the raw Request tab in Repeater.

2. Change the request path to GET /admin HTTP/2 and click Send. Verify you get a 200 OK.

3. Change the path to GET /admin/delete?username=carlos HTTP/2 and click Send.

4. The lab is successfully solved! 


**Key Takeaway / Mitigation:** If a server must use the jku header, it must strictly validate the URL against a hardcoded whitelist of trusted domains before fetching the key. Otherwise, ignore the jku header entirely and rely on a locally configured, trusted public key.




# 6TH LAB


# Lab: JWT authentication bypass via kid header path traversal
**Platform:** PortSwigger Web Security Academy
**Goal:** Use directory traversal in the `kid` header to force the server to use `/dev/null` as the verification key, sign a forged token with a null byte, and delete user `carlos`.
**Vulnerability:** Directory Traversal in JWT Header + Insecure JWT Implementation (The server blindly uses the file path provided in the `kid` header to fetch the secret key without sanitizing the input).

## The Concept (The "Black Hole" Attack)
The `kid` (Key ID) header parameter is often used to retrieve the correct verification key from a local database or filesystem. If this parameter is vulnerable to Path Traversal, an attacker can manipulate it to point to a predictable file.
By pointing the `kid` to `../../../../../../../dev/null` (a file on Linux systems that is always empty), the server reads an empty stream and effectively uses a Null Byte as the symmetric secret key. The attacker can then forge a token, sign it locally using a Base64 encoded Null Byte (`AA==`), and the server will successfully verify it.

##  Prerequisites
* Burp Suite with the **JWT Editor** extension installed.

##  Step-by-Step Exploitation

### Step 1: Create a Null Byte Symmetric Key
1. Go to the **JWT Editor Keys** tab in Burp.
2. Click **New Symmetric Key**.
3. Click **Generate** to create a template.
4. Replace the generated value of the `"k"` parameter with `"AA=="` (Base64 for a null byte).
   `"k": "AA=="`
5. Click **OK** to save the key.

### Step 2: Forge the Token
1. Intercept the `GET /my-account` request and send it to **Repeater**.
2. Go to the **JSON Web Tokens** tab.
3. In the **Header**, change the `"kid"` value to the path traversal payload:
   `"kid": "../../../../../../../dev/null"`
4. In the **Payload**, change `"sub": "wiener"` to `"sub": "administrator"`.

### Step 3: Sign and Bypass
1. Click the **Sign** button at the bottom of the JWT tab.
2. Select your newly created Null Byte Symmetric Key.
3. **CRITICAL:** Check the box that says **"Don't modify header"** (to prevent the extension from overwriting your directory traversal payload).
4. Click **OK**.

### Step 4: Privilege Escalation & Takedown
1. Switch to the raw **Request** tab in Repeater.
2. Change the request path to `GET /admin HTTP/2` and click **Send**. Verify you get a `200 OK`.
3. Change the path to `GET /admin/delete?username=carlos HTTP/2` and click **Send**.
4. The lab is successfully solved! 

---
**Key Takeaway / Mitigation:** Never pass user-controlled input directly to filesystem APIs. The `kid` parameter should strictly be treated as an opaque string identifier, not a file path. Validate it against a hardcoded list of allowed Key IDs.