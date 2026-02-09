# CSRF Vulnerability with No Defenses

##  Lab Description
This lab demonstrates a classic **Cross-Site Request Forgery (CSRF)** attack. The application's "Change Email" functionality is vulnerable because it relies solely on session cookies for authentication and lacks any anti-CSRF tokens.

## Objective
Create a malicious HTML page that, when viewed by a victim, forces their browser to change their email address on the vulnerable website without their consent.

##  The Vulnerability (Why it works?)
The application fails to distinguish between a legitimate user request and a forged one.

1.  **Session Management:** The site uses cookies to identify the logged-in user.
2.  **Browser Behavior:** When a browser makes a request to a site (even from a different tab or site), it **automatically attaches the cookies** associated with that site.
3.  **Missing Defense:** There is no **CSRF Token** (a secret, unpredictable code) in the form. The server blindly trusts any request that comes with a valid cookie.



##  The Exploit Payload

I create a "Trap" using an HTML form that targets the vulnerable endpoint and auto-submits using JavaScript.

```html
<form method="POST" action="[https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email](https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email)">
    <input type="hidden" name="email" value="hacker@evil.com">
</form>

<script>
    document.forms[0].submit();
</script>
```
## How the Payload Works:
1. form action="...": Points to the target website's "Change Email" URL.

2. method="POST": Matches the HTTP method expected by the server.

3. type="hidden": Hides the input field so the victim sees nothing (or a blank page).

4. document.forms[0].submit(): Automatically clicks the "Submit" button as soon as the page loads.

## Reproduction Steps
1. Analyze the Request:

Log in to the application.

Change your email and intercept the request using Burp Suite.

Observe that the request only contains the email parameter and the session cookie. No csrf_token is present.

2. Craft the Exploit:

Go to the Exploit Server.

In the Body section, paste the payload code (replace YOUR-LAB-ID with the actual lab URL).

3. Deliver the Attack:

Click "Store" to save the exploit.

Click "Deliver to victim" to simulate sending the link to a logged-in user.

4. Verify:

The victim's browser will load your exploit page.

The script will force a POST request to the main site.

The browser will attach the victim's session cookie.

The server will process the request and change the email to hacker@evil.com.

## Remediation (How to fix)
1. To prevent CSRF, the application should implement Anti-CSRF Tokens.

2. The server should generate a unique, unpredictable token for every session/form.

3. This token must be included as a hidden field in the form (<input type="hidden" name="csrf" value="...">).

4. The server must verify that the token in the request matches the token issued to the user.