#  CSRF Where Token Validation Depends on Request Method

##  Lab Description
This lab demonstrates a flawed implementation of CSRF protection. The application uses a CSRF token for its "Change Email" function, but the backend only validates the token when the request method is `POST`. It completely bypasses token validation if the request method is switched to `GET`.

## 🎯 Objective
Exploit the flawed CSRF validation by converting the `POST` request to a `GET` request, bypassing the token check, and forcing the victim to change their email address.

##  Vulnerability Analysis
Many web frameworks allow developers to read parameters without specifying the HTTP method (e.g., using `$_REQUEST` in PHP instead of `$_POST`). 

1. **The Guard is only at the Front Door:** The developer implemented CSRF protection, but the middleware or function checking the token only runs if `method == POST`.
2. **The Back Door is Open:** By intercepting the request and changing the HTTP method to `GET`, the parameters (`email`) move to the URL query string. The server processes the email change without ever checking for the CSRF token.

## 💣 The Exploit Payload

Since i are now using a `GET` request, i do not need to construct a complex HTML `<form>`. i simply need the victim's browser to make a GET request to the vulnerable URL. 

i can do this using a JavaScript redirect or an invisible image tag.

**Payload (JavaScript Redirect):**
```html
<script>
    // Redirects the victim to the GET request URL. The browser automatically attaches the session cookie.
    window.location.href = "[https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email?email=hacker@evil.com](https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email?email=hacker@evil.com)";
</script>
```
## Steps to Reproduce
1. Intercept and Analyze:

* Log in to your account (wiener:peter).

* Submit a request to change your email address.

* Intercept this request in Burp Suite. You will see it is a POST request with a csrf parameter in the body.

2. Test for Method Vulnerability:

* Send the intercepted request to Burp Repeater (Ctrl+R).

* Right-click on the request and select "Change request method". Burp will automatically convert it to a GET request and move the parameters to the URL.

* Remove the csrf parameter from the URL completely.

Click Send. If you get a 302 Found (redirect) instead of a CSRF error, the vulnerability exists!

3. Craft the Exploit:

* Go to the Exploit Server.

* Paste the Payload (JavaScript Redirect or Image tag) into the Body section.

* Replace YOUR-LAB-ID with your actual lab instance ID.

4. Deliver and Conquer:

* Click Store.

* Click Deliver to victim. The victim's email will be changed to hacker@evil.com, solving the lab.

## Remediation
To fix this, the backend must strictly enforce the HTTP method. The endpoint for changing an email should only accept POST requests. Any GET requests to this endpoint should be rejected with a 405 Method Not Allowed error. Additionally, CSRF token validation should be applied globally to all state-changing requests, regardless of the method used.