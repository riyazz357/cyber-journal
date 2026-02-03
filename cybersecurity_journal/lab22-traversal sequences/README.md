### Lab: Traversal sequences blocked with absolute path bypass

```markdown
#  Lab: File Path Traversal (Absolute Path Bypass)

| **Category** | Web Security / Directory Traversal |
| :--- | :--- |
| **Vulnerability Type** | Path Traversal |
| **Goal** | Retrieve `/etc/passwd` bypassing the traversal sequence block. |
| **Status** | ✅ Solved |

## 📖 Concept
The application attempts to prevent traversal by blocking or filtering the specific sequence `../`. However, it fails to validate if the user provides an **Absolute Path** (full path from the root directory). In Linux, an absolute path starts with a forward slash `/`.

## ⚔️ Exploitation Steps
1.  **Analysis:** The previous payload `../../../etc/passwd` failed because the application blocked the `../` characters.
2.  **Bypass Strategy:** Instead of navigating "backwards" using relative paths, i requested the file using its direct absolute location starting from the root directory (`/`).
3.  **Attack:**
    * Replaced filename with: `/etc/passwd`
4.  **Result:** The application treated it as a valid file path and returned the sensitive content.

## 🚀 Payload
```text
/etc/passwd
```