#  Lab: File Path Traversal (Validation of Start of Path)

| **Category** | Web Security / Directory Traversal |
| :--- | :--- |
| **Vulnerability Type** | Path Traversal |
| **Goal** | Retrieve `/etc/passwd` by adhering to the required start path. |
| **Status** | ✅ Solved |

##  Concept
The application enforces a security rule requiring the `filename` parameter to start with a specific expected base directory (e.g., `/var/www/images/`).
* **Bypass:** I supply the expected base path first to satisfy the filter, and then append traversal sequences (`../`) to step out of that directory and access the file system root.

##  Exploitation Steps
1.  **Analysis:** Observed that legitimate requests include the full directory path: `filename=/var/www/images/28.jpg`.
2.  **Bypass Strategy:** I kept the required prefix to pass the validation check.
3.  **Attack:**
    * Base Path: `/var/www/images/`
    * Traversal Payload: `../../../etc/passwd`
    * Combined Payload: `/var/www/images/../../../etc/passwd`
4.  **Result:** The application validated the start of the path successfully, then processed the `../` sequences to navigate back to the root and retrieve the password file.

##  Payload
```text
/var/www/images/../../../etc/passwd
```