#  Insecure Direct Object References (Static File IDOR)

##  Lab Description
This lab contains an **Insecure Direct Object Reference (IDOR)** vulnerability in the chat transcript download functionality. The application stores chat logs using predictable, incremental filenames (e.g., `1.txt`, `2.txt`) and allows users to download logs directly by requesting the filename, without verifying ownership.

##  Objective
Exploit the IDOR vulnerability to retrieve the chat transcript of another user (`carlos`), extract their password from the text, and log in to their account.

##  The Vulnerability (Predictable Resource Location)
When files are stored with sequential IDs (1, 2, 3...), an attacker can easily enumerate and access files belonging to others.
* **The Flaw:** The server retrieves the file based solely on the filename in the URL (`/download/2.txt`) and does not check if the requester participated in that specific chat session.
* **The Exploit:** Simply decrementing the file number allows access to previous chat logs.



##  Steps to Reproduce

1.  **Generate Traffic:**
    * Open the lab and access the **"Live Chat"** feature.
    * Send a message to the bot to create a chat session.
    * Click **"Download Transcript"**.

2.  **Analyze the Request:**
    * Inspect the download request in **Burp Suite** or the browser's download history.
    * Note the URL structure: `https://YOUR-LAB-ID.../download-transcript/2.txt`.
    * The filename (`2.txt`) suggests an incremental naming scheme.

3.  **Execute IDOR:**
    * Send the request to **Burp Repeater**.
    * Change the filename from `2.txt` to `1.txt` (guessing the previous transcript belongs to another user).
    * Click **Send**.

4.  **Extract Sensitive Info:**
    * Examine the response body. It contains the chat log of the user `carlos`.
    * Locate the password revealed in the conversation (e.g., "My password is...").

5.  **Account Takeover:**
    * Go to the **Login** page.
    * Log in using the username `carlos` and the extracted password.

##  Remediation
* **Use Indirect References:** Map internal file IDs (like `1.txt`) to random, unpredictable tokens (e.g., `download?token=x8z9...`) that are valid only for the user's session.
* **Access Control:** Always verify that the user requesting a file is the owner of that file before serving it.