#  User ID Controlled by Request Parameter (Unpredictable IDs)

##  Lab Description
This lab contains an **Insecure Direct Object Reference (IDOR)** vulnerability, but with a twist. Unlike simple predictable IDs (e.g., `id=101`), this application uses **Unpredictable IDs** (GUIDs/UUIDs) for user accounts. While the IDs cannot be guessed, they are leaked elsewhere in the application.

##  Objective
Find the unpredictable ID (GUID) of the user `carlos` by browsing the public areas of the site (like blog posts), use it to access his account page, and retrieve his API Key.

##  The Vulnerability (IDOR + Info Leak)
Using complex IDs (GUIDs) is a good defense against IDOR, but only if those IDs remain secret.
* **The Flaw:** The application exposes the user's GUID in public-facing URLs (e.g., filtering blog posts by author).
* **The Exploit:** An attacker can harvest these IDs from public pages and use them to access restricted account pages (`/my-account?id=...`), bypassing access controls.



##  Steps to Reproduce

1.  **Reconnaissance (The Hunt):**
    * Log in as `wiener`:`peter` to understand the URL structure (`/my-account?id=GUID`).
    * Navigate to the **Home** page to view blog posts.

2.  **Find the Leak:**
    * Locate a blog post written by the target user, **`carlos`**.
    * Click on the author's name (`carlos`).
    * Observe the URL in the address bar. It likely changes to something like:
      `/filter?userId=abc-123-def-456`

3.  **Capture the ID:**
    * Copy the `userId` value from the URL. This is Carlos's unique GUID.

4.  **Execute IDOR:**
    * Click on **"My Account"**.
    * In the URL bar, replace your `id` parameter with the copied ID of `carlos`.
    * Press **Enter**.

5.  **Exfiltrate Data:**
    * You are now viewing Carlos's account page.
    * Copy the **API Key** displayed on the screen.
    * Submit the key to solve the lab.

##  Remediation
* **Access Control:** Do not rely solely on the unpredictability of IDs. Always verify that the currently logged-in user has permission to access the requested ID.
    * `if (current_session.user_id != requested_id) { return 403 Forbidden; }`
* **Minimize Leaks:** Avoid exposing internal user IDs in public URLs if possible, or ensure those IDs cannot be used for privileged actions.