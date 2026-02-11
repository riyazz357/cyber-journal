#  Unprotected Admin Functionality with Unpredictable URL

##  Lab Description
This lab contains an unprotected admin panel. The application attempts to secure the panel by using an unpredictable, obfuscated URL (Security by Obscurity), assuming that attackers cannot guess the location. However, the URL is disclosed within the application's client-side code.

##  Objective
Locate the hidden admin panel URL by analyzing the page source code and delete the user `carlos`.

##  The Vulnerability (Source Code Disclosure)
"Security by Obscurity" is not a valid security control. Even if a URL is randomly generated (e.g., `/admin-x9z1a`), the browser needs to know this URL to function or render links.
* **The Flaw:** The developer included the admin URL in the HTML/JavaScript source code, likely to render the link dynamically for authorized users.
* **The Exploit:** Attackers can simply "View Source" to reveal hidden links that are not visible on the rendered page.

## Steps to Reproduce

1.  **Initial Reconnaissance:**
    * Open the lab application.
    * Attempt standard paths like `/admin` or check `robots.txt` (likely fails).

2.  **Source Code Analysis:**
    * Right-click on the homepage and select **"View Page Source"** (or press `Ctrl+U`).
    * Use the browser's Find function (`Ctrl+F`) to search for the keyword **"admin"**.

3.  **Locate the Leak:**
    * Identify a JavaScript script or HTML comment revealing the path.
    * *Example Finding:*
        ```javascript
        var adminPanelTag = document.createElement('a');
        adminPanelTag.setAttribute('href', '/admin-unpredictable-string');
        ```

4.  **Access and Exploit:**
    * Copy the discovered path (e.g., `/admin-unpredictable-string`).
    * Append it to the base URL in the address bar.
    * Access the Admin Panel and click **"Delete"** next to `carlos`.

##  Remediation
* **Access Control:** Never rely on hidden URLs. Implement strict authentication and authorization checks on the server-side for all sensitive endpoints.
* **Code Review:** Ensure sensitive paths are not hardcoded in client-side JavaScript accessible to all users.