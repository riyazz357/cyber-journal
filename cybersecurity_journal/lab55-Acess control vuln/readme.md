#  User ID Controlled by Request Parameter with Password Disclosure

##  Lab Description
This lab demonstrates a critical **Information Disclosure** vulnerability combined with **IDOR**. The application allows users to view other users' profile pages by manipulating the `id` parameter. Crucially, the application pre-fills the password input field with the user's current password in the HTML source, allowing an attacker to retrieve it.

##  Objective
Log in as a standard user, switch the `id` parameter to access the **Administrator's** account page, extract the administrator's password from the HTML source code, log in as the administrator, and delete the user `carlos`.

##  The Vulnerability (Pre-filled Password Fields)
It is a severe security malpractice to send a user's current password to the client-side, even if masked by `type="password"`.
* **The Flaw:** The server renders the HTML input tag with the sensitive data: `<input type="password" value="PLAINTEXT_PASSWORD">`.
* **The Exploit:** While the browser renders this as dots/asterisks, the plaintext password is clearly visible in the DOM / Page Source. An attacker accessing the page via IDOR can simply read the `value` attribute.



##  Steps to Reproduce

1.  **Login & Navigate:**
    * Log in with credentials `wiener`:`peter`.
    * Go to the **"My Account"** page.
    * URL Pattern: `.../my-account?id=wiener`

2.  **Execute IDOR:**
    * Change the URL parameter to `id=administrator`.
    * Press **Enter**. The page now displays the Administrator's profile.

3.  **Extract the Password:**
    * Locate the "Password" input field (masked with dots).
    * Right-click the field and select **"Inspect"** (or view Page Source).
    * Look for the `value` attribute in the HTML tag:
      `<input required type="password" name="password" value="ADMIN_PASSWORD_HERE">`
    * Copy the password.

4.  **Privilege Escalation:**
    * Click **"Log out"**.
    * Log in using the username `administrator` and the stolen password.

5.  **Complete the Mission:**
    * Access the **Admin Panel**.
    * Delete the user `carlos`.

##  Remediation
* **Never Pre-fill Passwords:** Password fields should always be empty when a profile page loads.
* **Access Control:** Ensure users can only view their own profile data (IDOR protection).
* **Separate Flows:** Use a separate, dedicated flow for changing passwords that requires entering the old password blindly, without the server sending it back.