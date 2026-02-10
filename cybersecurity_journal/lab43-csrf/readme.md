#  CSRF Where Token Validation Depends on Token Being Present

##  Lab Description
This lab contains a specific logic flaw in its Cross-Site Request Forgery (CSRF) protection mechanism. The application correctly validates the CSRF token **if** it is present in the request. However, if the `csrf` parameter is completely omitted from the request body, the validation logic is skipped entirely, allowing the request to proceed.

##  Objective
Exploit the conditional validation logic to perform a CSRF attack. The goal is to change the victim's email address by crafting a request that simply does not include the CSRF token.

##  The Vulnerability (The "Lazy Guard" Flaw)
The vulnerability lies in how the backend validates the token. The pseudocode likely looks like this:

```python
# Flawed Logic
if request.has_parameter("csrf"):
    if not validate(request.getParameter("csrf")):
        return Error("Invalid Token")
else:
    # Danger Zone: If parameter is missing, do nothing!
    pass 

process_email_change()
```
Because the validation is wrapped inside a condition that checks for the existence of the parameter, an attacker can bypass the check by simply removing the csrf parameter from the malicious form.

💣 The Exploit Payload
I create a standard HTML <form> that targets the vulnerable endpoint. Crucially, i exclude the csrf input field entirely.

```HTML
<form method="POST" action="[https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email](https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email)">
    <input type="hidden" name="email" value="hacker@evil.com">
</form>

<script>
    document.forms[0].submit();
</script>
```
## Steps to Reproduce
1. Analyze the Request:

* Log in to the application.

* Change your email address and intercept the request in Burp Suite.

* Note that the body contains email=...&csrf=....

2. Test the Flaw:

* Send the request to Burp Repeater.

* Delete the entire csrf parameter (and the preceding & symbol).

* The body should look like: email=test@test.com

* Click Send. If you receive a 302 Found response, the bypass works.

3. Craft the Exploit:

* Go to the Exploit Server.

* Paste the payload code into the Body section.

* Replace YOUR-LAB-ID with your actual lab instance ID.

4. Deliver the Attack:

* Click Store.

* Click Deliver to victim.

The victim's browser sends the POST request without the token, bypassing the check and changing their email.

# Remediation
* To fix this, the application must enforce CSRF validation on all state-changing requests unconditionally. The validation logic should assume the request is invalid unless a valid token is present and verified.

* Fix: Ensure the csrf parameter is mandatory. If it is missing, the server should reject the request immediately.