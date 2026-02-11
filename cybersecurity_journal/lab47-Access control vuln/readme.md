#  User ID Controlled by Request Parameter (IDOR)

##  Lab Description
This lab demonstrates a classic **Insecure Direct Object Reference (IDOR)** vulnerability. The application allows access to user account pages based solely on a user-controllable parameter (`id`) in the URL, without verifying if the logged-in user is authorized to access that specific account.

##  Objective
Log in as a standard user (`wiener`), manipulate the `id` parameter to access the account page of another user (`carlos`), and retrieve their API Key.

##  The Vulnerability (IDOR)
IDOR occurs when an application provides direct access to objects based on user-supplied input.
* **The Flaw:** The server trusts the client's input (`?id=username`) to decide which account to display.
* **The Exploit:** By simply changing the parameter value from the attacker's username to the victim's username, the attacker gains unauthorized access to the victim's sensitive data.



##  Steps to Reproduce

1.  **Login & Identify:**
    * Log in with the known credentials `wiener`:`peter`.
    * Observe the URL in the browser address bar after logging in.
    * *URL Pattern:* `.../my-account?id=wiener`

2.  **Manipulate the ID:**
    * In the address bar, change the `id` parameter value from `wiener` to `carlos`.
    * *New URL:* `.../my-account?id=carlos`
    * Press **Enter**.

3.  **Data Exfiltration:**
    * The application loads the account page for the user `carlos`.
    * Locate the text: "Your API Key is: ...".
    * Copy the API Key.

4.  **Solve the Lab:**
    * Click the **"Submit solution"** button.
    * Paste the stolen API Key to complete the challenge.

##  Remediation
* **Access Control Checks:** Implement server-side checks to ensure the logged-in user is authorized to access the requested object.
    * *Logic:* `if (requested_id == session.user_id) { show_data() } else { return 403_Forbidden }`
* **Use Indirect References:** Instead of using predictable IDs (like database keys or usernames) in URLs, use random, session-mapped tokens (Reference Map).