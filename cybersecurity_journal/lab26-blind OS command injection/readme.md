# Lab: Blind OS Command Injection (Output Redirection)

| **Category** | Web Security / OS Command Injection |
| :--- | :--- |
| **Vulnerability Type** | Blind OS Command Injection |
| **Goal** | Execute the `whoami` command and retrieve the output via a file. |
| **Status** | ✅ Solved |

## Concept
In "Blind" vulnerabilities, the application executes the injected command but does not return the output in the HTTP response.
To bypass this limitation, i use **Output Redirection**. I instruct the operating system to write the output of our command into a text file located in a web-accessible directory (like `/var/www/images/`). Once the file is created, i can retrieve it via a standard HTTP GET request.

* **Operator:** `>` (Redirects standard output to a file).
* **Target:** `/var/www/images/` (A directory usually writable by the web server).

## Exploitation Steps

### Phase 1: Injection (Writing the File)
1.  **Identify Point of Entry:** The `email` field in the feedback form is vulnerable.
2.  **Construct Payload:**
    * I chain the command using `||`.
    * I execute `whoami`.
    * I redirect output `>` to `/var/www/images/output.txt`.
3.  **Inject:**
    * Payload: `email=test@test.com||whoami>/var/www/images/output.txt||`
    * **Result:** The server processes the feedback and secretly creates `output.txt` in the images folder.

### Phase 2: Retrieval (Reading the File)
1.  **Locate Access Path:** I observed that product images are loaded via `filename` parameter (e.g., `/image?filename=53.jpg`).
2.  **Fetch the File:**
    * Modified the URL to point to our created file.
    * Payload: `filename=output.txt`
3.  **Result:** The browser displays the content of the file (the current user name, e.g., `runner` or `www-data`).

## 🚀 Final Payload used
```bash
|| whoami > /var/www/images/output.txt ||
```
