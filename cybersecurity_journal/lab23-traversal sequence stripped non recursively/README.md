# Lab: Traversal sequences stripped non-recursively

| **Category** | Web Security / Directory Traversal |
| :--- | :--- |
| **Vulnerability Type** | Path Traversal |
| **Goal** | Retrieve `/etc/passwd` bypassing the non-recursive filter. |
| **Status** | ✅ Solved |

## 📖 Concept
The application attempts to sanitize user input by removing directory traversal sequences (`../`). However, the filter is **Non-Recursive**, meaning it scans and removes the sequence only once.
* **Flaw:** If the attacker nests the sequence (e.g., `....//`), the filter removes the inner `../`, causing the remaining characters to collapse and form a valid `../` sequence again.



## ⚔️ Exploitation Steps
1.  **Analysis:** Standard `../` payloads are stripped, and absolute paths are blocked.
2.  **Bypass Strategy:** I used a **Nested Payload** technique.
    * Input: `....//`
    * Filter Action: Removes the middle `../`
    * Output: `../` (The valid traversal sequence remains).
3.  **Attack:**
    * Replaced filename with: `....//....//....//etc/passwd`
4.  **Result:** The application constructed the path successfully and returned the password file.

## 🚀 Payload
```text
....//....//....//etc/passwd
```