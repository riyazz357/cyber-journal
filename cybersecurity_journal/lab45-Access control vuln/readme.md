#  User Role Controlled by Request Parameter (Mass Assignment)

##  Lab Description
This lab demonstrates a **Mass Assignment** vulnerability where the application blindly binds user input to internal objects. The user profile update function accepts a JSON object but fails to whitelist which fields can be updated. This allows a standard user to inject the `roleid` parameter and escalate privileges.

##  Objective
Log in as a standard user, modify the profile update request to include `"roleid": 2` (Admin role), and use the new privileges to delete user `carlos`.

##  The Vulnerability (Mass Assignment)
Modern frameworks often allow developers to automatically bind HTTP request parameters to code variables or database objects.
* **The Flaw:** If the developer writes code like `User.update(request.body)` without filtering, the attacker can update *any* field in the User table, including sensitive fields like `role`, `isAdmin`, or `balance`.

##  Steps to Reproduce

1.  **Login & Intercept:**
    * Log in with credentials `wiener`:`peter`.
    * Navigate to the **"My Account"** page.
    * Enter a new email address and click **"Update email"**.
    * Intercept this request using **Burp Suite**.

2.  **Analyze the Request:**
    * Send the request to **Burp Repeater**.
    * Observe the body is a JSON object: `{"email": "..."}`.

3.  **Inject the Payload:**
    * Modify the JSON to include the administrative role ID. In this lab, the Admin `roleid` is `2`.
    * **Modified Payload:**
        ```json
        {
            "email": "hacker@evil.com",
            "roleid": 2
        }
        ```
    * Click **Send**.

4.  **Verify & Exploit:**
    * Review the server response. It should reflect the user object with the updated `roleid`.
    * Refresh the page in the browser.
    * Access the newly visible **"Admin Panel"** link (or navigate to `/admin`).
    * Delete the user `carlos`.

##  Remediation
* **Use Data Transfer Objects (DTOs):** Instead of binding request data directly to database entities, use a separate object that only contains the fields allowed to be updated (e.g., `UpdateEmailRequest`).
* **Whitelisting:** Explicitly specify which fields can be updated from the request.
    * *Bad:* `user.update(request.all())`
    * *Good:* `user.email = request.input('email')`