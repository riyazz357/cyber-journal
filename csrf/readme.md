#  Master Notes: Cross-Site Request Forgery (CSRF) Deep Dive

A comprehensive, master-level guide to understanding, exploiting, and defending against Cross-Site Request Forgery (CSRF). Created for Security Engineers, Pentesters, and Bug Bounty Hunters.

---

##  Table of Contents
1. [What is CSRF?](#1-what-is-csrf)
2. [Core Concept Behind CSRF](#2-core-concept-behind-csrf)
3. [Technical Conditions Required](#3-technical-conditions-required)
4. [Step-by-Step Attack Flow](#4-step-by-step-attack-flow)
5. [Why SOP Does NOT Stop CSRF](#5-why-same-origin-policy-sop-does-not-stop-csrf)
6. [Simple vs. Non-Simple Requests](#6-simple-vs-non-simple-requests-cors)
7. [GET vs. POST CSRF](#7-get-vs-post-csrf)
8. [CSRF vs. XSS Comparison](#8-csrf-vs-xss-the-ultimate-comparison)
9. [Advanced Types of CSRF](#9-advanced-types-of-csrf)
10. [Protection Mechanisms](#10-protection-mechanisms-defense)
11. [Common Bypass Techniques](#11-common-bypass-techniques-for-hunters)
12. [When CSRF is NOT Possible](#12-when-csrf-is-not-possible)
13. [Bug Bounty Testing Checklist](#13-real-world-testing-checklist)
14. [Interview Questions & Answers](#14-master-level-interview-questions)

---

## 1. What is CSRF?
**Cross-Site Request Forgery (CSRF)** is a web security vulnerability that allows an attacker to induce users to perform actions that they do not intend to perform. It exploits the trust a web application has in an authenticated user's browser.

**The Analogy:** Imagine you are logged into your bank. An attacker hands your browser a forged check and says, "Deposit this." Because your browser has your "signature" (Session Cookie), it blindly submits it to the bank. The bank sees your valid signature and executes the transfer.

---

## 2. Core Concept Behind CSRF
CSRF exists because of **Ambient Credentials**.
* Browsers automatically include certain credentials (like Cookies and HTTP Basic Auth) in cross-origin requests.
* The server blindly trusts these cookies for authentication.
* **Crucial Fact:** The attacker **does not need to steal your cookies**. They only need your browser to send the request *for* them.

---

## 3. Technical Conditions Required
For a classic CSRF attack to be viable, **ALL THREE** conditions must be met:
1.  **State-Changing Action:** An action the attacker wants to induce (e.g., changing password, transferring funds).
2.  **Cookie-Based Session Handling:** The application relies on session cookies (not `Authorization: Bearer` headers).
3.  **No Unpredictable Parameters:** The request cannot require data the attacker cannot guess (like a random CSRF token or current password).

---

## 4. Step-by-Step Attack Flow



1.  **Victim Logs In:** Authenticates to `bank.com`. Server sets a session cookie (`Set-Cookie: sessionid=ABC`).
2.  **Victim Visits Malicious Site:** Attacker tricks victim into visiting `evil.com`.
3.  **Payload Executes:** `evil.com` contains a hidden auto-submitting form targeting `bank.com/transfer`.
4.  **Browser Attaches Cookies:** The browser sees a request going to `bank.com` and automatically attaches `sessionid=ABC`.
5.  **Server Executes:** The bank verifies the cookie and transfers the money.

---

## 5. Why Same-Origin Policy (SOP) Does NOT Stop CSRF
* **SOP** prevents a website from **READING** data from another origin.
* **CSRF** is a **WRITE-ONLY** attack. 
* The attacker forces your browser to fire a gun (send a POST request), but because of SOP, they cannot see if the bullet hit the target (cannot read the response). For CSRF, the attacker only cares that the state-changing action occurred.

---

## 6. Simple vs. Non-Simple Requests (CORS)

### A. Simple Requests (Dangerous)
Browsers send these cross-origin **without** asking the server for permission.
* **Methods:** `GET`, `POST`, `HEAD`
* **Content-Types:** `application/x-www-form-urlencoded`, `multipart/form-data`, `text/plain`

### B. Non-Simple Requests (Triggers Preflight)
Browsers send an `OPTIONS` request first to check permissions.
* **Methods:** `PUT`, `DELETE`, `PATCH`
* **Content-Types:** `application/json`
* **Custom Headers:** `X-Requested-With`

---

## 7. GET vs. POST CSRF
* **GET-Based:** Extremely dangerous. Triggered with zero clicks using a simple image tag: `<img src="https://bank.com/transfer?amount=1000&to=hacker">`. State-changing actions should *never* use GET.
* **POST-Based:** Requires hidden forms and JavaScript to auto-submit, but still highly exploitable.

---

## 8. CSRF vs. XSS: The Ultimate Comparison



| Feature | CSRF | XSS |
| :--- | :--- | :--- |
| **Execution Context** | Attacker's site. | Target's site. |
| **Goal** | Force action execution. | Inject scripts to steal data/sessions. |
| **Read Response?** | ❌ No (Blocked by SOP). | ✅ Yes. |
| **Requires Login?** | ✅ Yes (Usually). | ❌ Not strictly required. |
| **Relationship** | **If a site has XSS, CSRF protections (like tokens) are useless.** |

---

## 9. Advanced Types of CSRF
1.  **Login CSRF:** Forcing the victim to log into the *attacker's* account (used for tracking/search history poisoning).
2.  **JSON CSRF:** Exploiting servers that accept JSON but fail to validate the `Content-Type` header (sending JSON as `text/plain` via a form).

---

## 10. Protection Mechanisms (Defense)

### 1. Synchronizer Token Pattern (Stateful)

The server generates a cryptographically strong, random token, saves it in the session, and embeds it into forms. The attacker cannot read this token due to SOP.

### 2. Double Submit Cookie Pattern (Stateless)
The server sends a random token as a cookie and requires the exact same token in a hidden form field. Weakness: Vulnerable to Subdomain Takeover.

### 3. SameSite Cookie Attribute

* `Strict`: Cookies NEVER sent cross-site. (Maximum security).
* `Lax`: Cookies sent on top-level navigations but blocked on background POSTs. (Modern default).
* `None`: Cookies always sent. (Requires `Secure` flag).

### 4. Origin & Referer Validation
Server checks `Origin` or `Referer` HTTP headers. Best used as Defense-in-Depth, not sole protection.

---

## 11. Common Bypass Techniques (For Hunters)
1.  **Remove the Token:** Delete the `csrf_token` parameter entirely.
2.  **Method Swapping:** Change a `POST` request to a `GET` request.
3.  **Token Type Confusion:** Submit an empty token or an array (`csrf_token[]=...`).
4.  **Extract via XSS:** Use an existing XSS vulnerability to scrape the token from the DOM and fire the AJAX request.

---

## 12. When CSRF is NOT Possible
* Applications relying entirely on Custom Headers (e.g., `Authorization: Bearer <JWT>`).
* `SameSite=Strict` is universally enforced.
* The action requires unpredictable data (e.g., entering the current password).

---

## 13. Real-World Testing Checklist
- [ ] Identify state-changing actions (email change, fund transfer).
- [ ] Verify if authentication relies on Cookies.
- [ ] Inspect the session cookie's `SameSite` attribute.
- [ ] Drop the CSRF token parameter and test.
- [ ] Modify the CSRF token value and test.
- [ ] Change the request method from POST to GET.
- [ ] Change `Content-Type` from `application/json` to `text/plain`.
- [ ] Test for Login CSRF on authentication endpoints.

---

## 14. Master-Level Interview Questions

**Q1: What is the fundamental difference between SOP and CSRF?**
*Answer:* SOP prevents a malicious origin from *reading* data from another origin. CSRF exploits the browser to *write/send* data to another origin. SOP does not block the sending of the request.

**Q2: Can an attacker use CSRF to steal a user's sensitive data?**
*Answer:* Generally, no. CSRF forces an action but cannot read the server's response due to SOP. Data theft usually requires XSS.

**Q3: Is CSRF possible if an application uses JWTs?**
*Answer:* Yes, if the JWT is stored in an `HttpOnly` Cookie. If it is stored in `localStorage` and attached via JavaScript to the `Authorization` header, traditional CSRF is impossible.

**Q4: Is CSRF possible if an application uses JWTs?** 
Answer: It depends entirely on where the JWT is stored. If the JWT is stored in an HttpOnly Cookie, the browser will auto-attach it, making CSRF possible. If it is stored in localStorage and attached via JavaScript to the Authorization header, traditional CSRF is impossible.

**Q5: How does the Double Submit Cookie pattern work, and what is its main weakness?**
Answer: It relies on sending a random value in both a cookie and a request parameter. The server verifies they match. Its main weakness is that if an attacker compromises a subdomain (Subdomain Takeover), they can set cookies for the parent domain, thereby supplying their own matching cookie and parameter to bypass the check.
---

## Documented by:*mohammad riyaz*