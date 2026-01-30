# 💻 Lab: OS Command Injection, Simple Case

| **Category** | Web Security / OS Command Injection |
| :--- | :--- |
| **Vulnerability Type** | Remote Code Execution (RCE) |
| **System** | Linux |
| **Tools Used** | Burp Suite (Repeater) |
| **Status** | ✅ Solved |

---

## 📖 Conceptual Overview

**OS Command Injection** (also known as Shell Injection) is a web security vulnerability that allows an attacker to execute arbitrary operating system (OS) commands on the server that is running an application.

In this scenario, the application takes user input (Product Store ID) and passes it directly to a system shell command without proper validation. This allows us to "break out" of the intended command and chain our own malicious commands.

---

## 🕵️‍♂️ Phase 1: Analysis & Detection

### 1. Functionality Check
The application has a "Check Stock" feature. When a user checks stock for a product, the application sends a POST request with parameters like `productId` and `storeId`.

* **Request:** `storeId=1`
* **Backend Logic (Hypothetical):**
    ```bash
    stock_check_script.sh 1
    ```

### 2. Injection Point Identification
I tested the `storeId` parameter to see if it accepts shell metacharacters.
* **Payload:** `1|whoami`
* **Concept:** The pipe character `|` in Linux chains commands. It takes the output of the first command (if any) and passes it to the second.

---

## ⚔️ Phase 2: Exploitation (RCE)

I successfully executed the `whoami` command to retrieve the current user of the server.

### The Payload:
I modified the `storeId` parameter in the POST request:

```text
storeId=1|whoami
```

## Execution Flow:
1. Original Command: stock_check_script.sh 1

2. Injected Command: stock_check_script.sh 1|whoami

3. Server Action:

    The server executes the stock check script.

    Then, due to the pipe |, it executes whoami.

4. Response: The application returned the stock levels AND the username of the server (e.g., peter-IlY2...).

## Remediation
**To prevent OS Command Injection:**

1. Avoid System Calls: If possible, use built-in language APIs instead of calling OS commands (e.g., use Python's os.listdir() instead of ls).

2. Input Validation: Strictly validate user input against a whitelist (e.g., ensure storeId is only an integer).

3. Parameterized Functions: If system calls are necessary, use functions that separate the command from the arguments (like subprocess.run() in Python with shell=False).