#  Master Notes: Web Authentication & Security

A comprehensive deep dive into Authentication mechanisms, common vulnerabilities, and secure implementation patterns for modern web applications.

> **Note:** This repository is for educational purposes and cybersecurity research.

---

##  Table of Contents
- [1. Authentication vs. Authorization](#1-authentication-vs-authorization)
- [2. Common Mechanisms](#2-common-authentication-mechanisms)
- [3. Session-Based Authentication](#3-session-based-authentication-stateful)
- [4. Password Reset Vulnerabilities](#4-password-reset-vulnerabilities)
- [5. Multi-Factor Authentication (2FA)](#5-multi-factor-authentication-2fa)
- [6. JWT (JSON Web Token) Security](#6-jwt-json-web-token-authentication)
- [7. Secure Implementation Checklist](#7-secure-implementation-summary)

---

## 1. Authentication vs. Authorization

Before exploiting, distinguish between identity and permission.

| Feature | **Authentication (AuthN)** | **Authorization (AuthZ)** |
| :--- | :--- | :--- |
| **Question** | "Who are you?" | "What are you allowed to do?" |
| **Analogy** | Showing ID at the gate. | Using a key card for the CEO's office. |
| **Mechanism**| Passwords, OTP, Biometrics. | Permissions, Roles (RBAC), ACLs. |
| **Failure** | **Account Takeover (ATO)** | **Privilege Escalation / IDOR** |

---

## 2. Common Authentication Mechanisms
1.  **Username + Password:** Classic method (hashes required).
2.  **Session-based:** Server stores state (Stateful).
3.  **Token-based (JWT):** Client stores state (Stateless).
4.  **2FA:** Something you know + Something you have.
5.  **OAuth / SSO:** Delegated auth (Google/Facebook).

---

## 3. Session-Based Authentication (Stateful)

###  The Flow
1.  **User Logs in** with credentials.
2.  **Server** verifies and creates a `Session ID` in the database.
3.  **Server** sends ID via `Set-Cookie` header.
4.  **Browser** sends this Cookie automatically with every request.

###  Vulnerabilities & Fixes

#### A. Session Fixation
* **Attack:** Attacker tricks victim into logging in using a Session ID known to the attacker.
* **Exploit:** `site.com/login?session_id=123` -> Victim logs in -> Attacker uses ID `123` to hijack.
* ** Fix:** Always use `session_regenerate_id()` immediately after login.

#### B. Session Hijacking
* **Attack:** Stealing the cookie via XSS or Network Sniffing.
* ** Fix:** Use `HttpOnly` (No JS access) and `Secure` (HTTPS only) flags.

---

## 4. Password Reset Vulnerabilities
The "Forgot Password" feature is a prime target for Account Takeover (ATO).

###  Common Attack Vectors
1.  **Host Header Poisoning:**
    * Request: `Host: evil.com`
    * Result: Email link points to `evil.com/token=123`. Token leaked to attacker.
2.  **Predictable Tokens:** Using timestamps or sequential IDs (`1001` -> `1002`).
3.  **No Expiration:** Old tokens remain valid forever.

###  Secure Design
* Use **CSPRNG** (Cryptographically Secure Pseudo-Random Number Generator).
* Tokens must expire in **10-15 minutes**.
* **Single Use:** Destroy token immediately after use.

---

## 5. Multi-Factor Authentication (2FA)

###  Bypass Techniques
* **Response Manipulation:** Intercept HTTP `403 Forbidden` and change to `200 OK`.
* **Forced Browsing:** Skip the OTP page and manually navigate to `/dashboard` or `/profile` endpoints.
* **Race Conditions:** Using tools like **Turbo Intruder** to send 100 requests simultaneously to bypass rate limits.

---

## 6. JWT (JSON Web Token) Authentication
JWT is **Stateless**. The token *is* the session.

###  Structure
`Header.Payload.Signature`

```json
// Header
{ "alg": "HS256", "typ": "JWT" }
// Payload
{ "user_id": 105, "role": "admin" }
// Signature
HMACSHA256(base64(Header) + "." + base64(Payload), SECRET)

```
###  JWT Attacks (Deep Dive)

#### 1. The 'None' Algorithm Attack
* **Concept:** Some JWT libraries support an insecure debugging algorithm called `none` (no signature).
* **Attack Vector:**
    1.  Attacker captures a valid token.
    2.  Modifies Header to: `{"alg": "none"}`.
    3.  Removes the entire Signature section.
    4.  Modifies Payload to elevate privileges (e.g., `"role": "admin"`).
* **Flaw:** The backend server sees `alg: none` and skips the signature verification process, accepting the forged token.

#### 2. Key Confusion Attack (RS256 → HS256)
* **Scenario:** The server is configured to use **RS256** (Asymmetric: Private Key to sign, Public Key to verify).
* **Attack Vector:**
    1.  Attacker obtains the server's **Public Key** (often available at `/.well-known/jwks.json`).
    2.  Attacker changes the token Header to `HS256` (Symmetric).
    3.  Attacker signs the malicious token using the server's **Public Key** as the HMAC "secret".
* **Result:** The server receives `HS256`, gets confused, and uses its own Public Key to verify the signature (thinking it's the shared secret). The math checks out, and the token is accepted.



#### 3. Weak Secret Brute Force
* **Concept:** If the server uses **HS256** with a weak secret key (e.g., `secret123`, `companyname2023`).
* **Attack Vector:**
    1.  Attacker captures a token.
    2.  Uses tools like **Hashcat** or **John the Ripper** to brute-force the signature offline.
    3.  Once the secret is cracked, the attacker can generate valid tokens for any user forever.

---

## 7. Secure Implementation Summary

### For Developers & Pentesters:

1.  **Hardcode Algorithms:**
    * **Never trust the `alg` header.**
    * Explicitly force the backend verification logic to use `RS256` or `HS256` only.
    * Reject any token with `alg: none`.

2.  **Validate Standard Claims:**
    * **`exp` (Expiration):** Reject tokens that have expired.
    * **`iss` (Issuer):** Ensure the token was created by your auth server.
    * **`aud` (Audience):** Ensure the token is intended for your application.

3.  **Short Access Tokens:**
    * Access Tokens should have a short lifespan (**15 minutes max**).
    * Use **Refresh Tokens** stored in `HttpOnly` cookies for maintaining long-term sessions.

4.  **No Blind Trust (AuthN != AuthZ):**
    * **JWT proves Identity, not Authority.**
    * Just because a token says `role: admin`, doesn't mean the user is still an admin.
    * **Critical Actions:** Always validate permissions against the database before performing sensitive operations (e.g., deleting data).

5.  **Token Rotation:**
    * Implement **Refresh Token Rotation**.
    * If a used refresh token is presented again, invalidate the entire token family to detect and stop token theft.

# common questions and concepts

## 8. Common Security Interview Questions

### Q1: Why must a session ID be regenerated after login?
**Answer:**
To prevent **Session Fixation** attacks. If the ID is not regenerated, an attacker can trick a victim into authenticating with a known Session ID, allowing the attacker to hijack the session immediately.



### Q2: What are the 3 mandatory properties of a secure password reset token?
**Answer:**
1.  **Cryptographically Random:** Unpredictable (CSPRNG).
2.  **Short Expiry:** Valid for only 10-15 minutes.
3.  **Single Use:** Invalidated immediately after use.

### Q3: Why must 2FA validation be server-side?
**Answer:**
Because **Client-Side Validation** (JavaScript checks) can be easily bypassed by an attacker using tools like Burp Suite to modify the response or by directly forcing the browser to navigate to protected endpoints.



### Q4: What is the purpose of JWT signature verification?
**Answer:**
To ensure the token was issued by the legitimate server and has **not been tampered with** by the client. Without signature verification, anyone can modify the payload (e.g., change `role: user` to `role: admin`).



### Q5: Can a weak JWT secret lead to account takeover?
**Answer:**
**Yes.** If the HMAC secret (used in HS256) is weak (e.g., "secret123"), an attacker can brute-force it offline using tools like Hashcat. Once cracked, they can sign their own forged tokens with Admin privileges.

### Q6: What is a Key Confusion Attack?
**Answer:**
An attack where the attacker changes the JWT header algorithm from **RS256** (Asymmetric) to **HS256** (Symmetric) and signs the token using the server's **Public Key** as the HMAC secret. The server, confused by the header, verifies the signature using its own public key and accepts the forged token.

### Q7: If the server re-checks the user role from the database, does a forged JWT role work?
**Answer:**
**No.** This is the best defense. Even if the JWT says `role: admin`, the server-side database check (`SELECT role FROM users WHERE id = ?`) is the source of truth and will override the forged claim.

### Q8: What is the most dangerous authentication vulnerability?
**Answer:**
**Authentication Bypass via Improper Signature Verification** (e.g., `alg: none` or missing verification). This is critical because it allows full **Privilege Escalation** (Account Takeover) without needing any credentials.


## Documented by: *Mohammad Riyaz*