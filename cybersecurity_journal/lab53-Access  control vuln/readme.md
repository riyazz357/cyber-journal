#  User ID Controlled by Request Parameter with Data Leakage in Redirect

##  Lab Description
This lab demonstrates a subtle **Access Control** vulnerability where the server correctly identifies an unauthorized access attempt and redirects the user. However, due to a flaw in the execution order, the server generates and sends the sensitive data in the response body *before* instructing the browser to redirect.

##  Objective
Log in as `wiener`, attempt to access `carlos`'s account page, intercept the redirect response, and extract the sensitive API Key hidden in the response body.

##  The Vulnerability (Data Leakage in 302 Redirect)
Browsers automatically follow `302 Found` (Redirect) responses and discard the body of the response. Developers often assume this makes the data safe.
* **The Flaw:** The application writes sensitive data (the victim's profile) to the response stream *before* enforcing the access control check (the redirect).
* **The Exploit:** An attacker using a proxy (like Burp Suite) can inspect the raw HTTP response. Even though the browser would ignore it, the data is present in the response body.



##  Steps to Reproduce

1.  **Login & Intercept:**
    * Log in with credentials `wiener`:`peter`.
    * Click on **"My Account"**.
    * Capture this request in **Burp Suite**.

2.  **Modify the Request:**
    * Send the request to **Burp Repeater**.
    * Change the user parameter from `id=wiener` to `id=carlos`.

3.  **Inspect the Response:**
    * Click **Send**.
    * Observe the response status is `302 Found` (Redirect to login/home).
    * **Crucial Step:** Do not follow the redirect. Instead, look at the **Response Body** in Repeater.

4.  **Extract Data:**
    * Scroll down through the HTML in the response body.
    * Even though the user is being redirected, the server has already printed the profile information.
    * Find the string: `"Your API Key is: ..."`.
    * Copy the key.

5.  **Solve the Lab:**
    * Submit the stolen API Key to complete the challenge.

##  Remediation
* **Fail Fast:** Perform access control checks (Authorization) *before* fetching or generating any sensitive data.
* **Stop Execution:** Ensure that after sending a redirect command, the code execution terminates immediately (e.g., using `die()` or `exit()` in PHP) so no further content is sent.