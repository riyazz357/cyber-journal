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