# Unprotected Admin Functionality (robots.txt Disclosure)

##  Lab Description
This lab contains an unprotected admin panel. The application attempts to keep the panel hidden by not linking to it from the main interface. However, the sensitive path is inadvertently disclosed in the `robots.txt` file, which is publicly accessible.

##  Objective
Find the hidden administration panel by inspecting the `robots.txt` file and delete the user `carlos`.

##  The Vulnerability (Information Disclosure)
`robots.txt` is a standard file used by websites to communicate with web crawlers (like Googlebot). It tells them which pages *not* to visit.
* **The Flaw:** By listing the admin panel in `robots.txt` (e.g., `Disallow: /administrator-panel`), the developer effectively announces the location of the secret panel to anyone who checks the file.
* **Security Principle Violated:** "Security by Obscurity". Hiding a URL is not a substitute for proper access control.



##  Steps to Reproduce

1.  **Reconnaissance:**
    * Open the lab application.
    * In the browser's address bar, append `/robots.txt` to the base URL.
    * *Example:* `https://YOUR-LAB-ID.web-security-academy.net/robots.txt`

2.  **Analyze the File:**
    * Observe the content of the file. Look for the `Disallow` directive.
    * *Finding:* `Disallow: /administrator-panel`

3.  **Exploit:**
    * Copy the disallowed path (`/administrator-panel`).
    * Replace `/robots.txt` in the URL bar with this path.
    * Press Enter. You will bypass the UI restrictions and access the admin panel directly.

4.  **Execute Action:**
    * Locate the user `carlos`.
    * Click the **"Delete"** button to solve the lab.

##  Remediation
* **Proper Authorization:** Always verify user permissions on the server-side before serving sensitive pages.
* **Avoid Leaks:** Do not list sensitive administrative paths in `robots.txt` if they are not protected by authentication.