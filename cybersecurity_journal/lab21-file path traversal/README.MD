#  Lab: File Path Traversal (Simple Case)

| **Category** | Web Security / Directory Traversal |
| :--- | :--- |
| **Vulnerability Type** | Path Traversal |
| **Goal** | Retrieve the content of the `/etc/passwd` file. |
| **Status** | ✅ Solved |

##  Concept
The application loads images using a filename parameter (e.g., `?filename=image.jpg`). It does not validate if the user is requesting a file outside the intended image directory. I use **Relative Path** sequence (`../`) to step back out of the folder and access system files.

## ⚔️ Exploitation Steps
1.  **Analysis:** Observed the URL parameter `filename=53.jpg`.
2.  **Payload Construction:** Used `../` to move up the directory tree to the root.
    * Typical Linux web root is `/var/www/html/`. I need to go back 3 levels to reach root `/`.
3.  **Attack:**
    * Replaced filename with: `../../../etc/passwd`
4.  **Result:** Server returned the content of the password file (e.g., `root:x:0:0...`).

##  Payload
```text
../../../etc/passwd
```
