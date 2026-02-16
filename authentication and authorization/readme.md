# 🔐 Master Notes: Web Authentication & Security

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