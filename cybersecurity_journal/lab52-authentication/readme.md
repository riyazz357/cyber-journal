#  Username Enumeration via Different Responses

##  Lab Description
This lab contains a logic flaw in its authentication mechanism. When a user attempts to log in, the server responds with different error messages depending on whether the username exists in the database or not. This allows an attacker to enumerate valid usernames and then brute-force the password.

##  Objective
1.  Enumerate a valid username from a provided list by analyzing server responses.
2.  Brute-force the password for that valid username to access the account.

##  The Vulnerability (The "Poker Face" Fail)
A secure login page should return a generic error like *"Invalid username or password"* for all failed attempts.
* **The Flaw:** The application returns *"Invalid username"* if the user doesn't exist, but returns *"Incorrect password"* if the user **does** exist.
* **The Exploit:** An attacker can use a list of common usernames to identify valid accounts based on the error message change.



##  Steps to Reproduce

1.  **Capture the Request:**
    * Attempt to log in with a random username and password.
    * Intercept the request in **Burp Suite** and send it to **Intruder**.

2.  **Enumerate Usernames (Sniper Attack):**
    * **Positions:** Clear all markers (`§`). Highlight the `username` value and click **Add §**.
    * **Payloads:** Load the list of candidate usernames.
    * **Start Attack:** Analyze the results. Look for a response with a different **Length** or **Status Code**.
    * *Observation:* One response contains the text **"Incorrect password"** (instead of "Invalid username"). Note this username.

3.  **Brute-Force Password:**
    * **Positions:** Update the `username` field with the valid username found in Step 2.
    * Highlight the `password` value and click **Add §**.
    * **Payloads:** Load the list of candidate passwords.
    * **Start Attack:** Look for a `302 Found` status code (indicating a successful login).

4.  **Login:**
    * Use the discovered username and password to log in and solve the lab.

##  Remediation
* **Generic Errors:** Always use the same error message (e.g., "Invalid credentials") regardless of whether the username or password was incorrect.
* **Timing Analysis:** Ensure the server takes the same amount of time to process valid and invalid usernames to prevent timing-based enumeration.