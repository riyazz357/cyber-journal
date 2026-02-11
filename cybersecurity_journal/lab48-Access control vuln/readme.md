#  User Role Controlled by Request Parameter (Cookie Tampering)

##  Lab Description
This lab demonstrates a critical **Broken Access Control** vulnerability. The application relies on a client-side cookie to determine the user's privilege level. Since cookies are stored in the user's browser, they can be easily modified by an attacker to escalate privileges.

##  Objective
Log in as a standard user (`wiener`), modify the session cookie to impersonate an administrator, and delete the user `carlos`.

##  The Vulnerability (Insecure Direct Object Reference / Parameter Tampering)
Trusting client-side input for security decisions is a major flaw.
* **The Flaw:** The server reads the `Admin` cookie from the request and grants access based solely on its value (`true` or `false`) without verifying it against a secure session on the server.
* **The Exploit:** An attacker can simply edit the cookie value using browser developer tools or a proxy like Burp Suite.



##  Steps to Reproduce

1.  **Login & Inspect:**
    * Log in with credentials `wiener`:`peter`.
    * Open browser **Developer Tools** (Press `F12` or Right-click -> Inspect).
    * Navigate to the **Application** tab (or "Storage" in Firefox) > **Cookies**.

2.  **Identify the Weakness:**
    * Observe the cookies set by the application.
    * Notice a cookie named `Admin` with the value `false`.

3.  **Tamper the Data:**
    * Double-click the value `false` and change it to `true`.
    * Alternatively, use **Burp Suite** to intercept a request and modify `Cookie: Admin=false` to `Cookie: Admin=true`.

4.  **Escalate & Attack:**
    * Refresh the page.
    * The application now treats you as an administrator.
    * Click on the newly visible **"Admin Panel"** link (or navigate to `/admin`).
    * Delete the user `carlos`.

##  Remediation
* **Server-Side Session Management:** Store user privileges (roles) in a secure server-side session, not in client-side cookies.
* **Integrity Checks:** If client-side tokens are necessary (like JWTs), they must be cryptographically signed so that any modification invalidates them.