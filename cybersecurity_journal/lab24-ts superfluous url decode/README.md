# Lab: Traversal sequences stripped with superfluous URL-decode

| **Category** | Web Security / Directory Traversal |
| :--- | :--- |
| **Vulnerability Type** | Path Traversal |
| **Goal** | Retrieve `/etc/passwd` by bypassing filters using Double URL Encoding. |
| **Status** | ✅ Solved |

##  Concept
Some web servers perform a security check to block directory traversal sequences (`../`). However, if the application performs a **Superfluous (Extra) URL-Decode** on the input *after* the security check, attackers can bypass the filter.
* **Mechanism:** I **Double Encode** the payload.
    1.  The security filter decodes it once: `%252e` $\rightarrow$ `%2e`. The filter sees `%2e%2e%2f` (which is just text strings to it, not a path traversal command) and lets it pass.
    2.  The application backend then decodes it again: `%2e%2e%2f` $\rightarrow$ `../`. The traversal executes.



## ⚔️ Exploitation Steps
1.  **Analysis:** Standard `../` and single-encoded `%2e%2e%2f` payloads were blocked by the WAF/Filter.
2.  **Bypass Strategy:** I used **Double URL Encoding**.
    * Target: `../../../etc/passwd`
    * Single Encode: `%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd`
    * Double Encode: `%252e%252e%252f%252e%252e%252f%252e%252e%252fetc/passwd`
3.  **Attack:** Injected the double-encoded string into the filename parameter.
4.  **Result:** The server decoded the input twice, reconstructing the traversal path and revealing the `/etc/passwd` file.

## 🚀 Payload
```text
%252e%252e%252f%252e%252e%252f%252e%252e%252fetc/passwd
```