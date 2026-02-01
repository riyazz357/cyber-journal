### 4. Lab: SQL Injection UNION Attack (Retrieving Data from Other Tables)

```markdown
#  Lab: SQL Injection UNION Attack (Retrieving Data from Other Tables)

| **Category** | Web Security / SQL Injection |
| :--- | :--- |
| **Vulnerability Type** | UNION-Based SQLi |
| **Goal** | Extract usernames and passwords from the `users` table. |
| **Tools Used** | Burp Suite |
| **Status** | ✅ Solved |

---

## Conceptual Overview
Once the column count and data types are mapped, an attacker can use the `UNION` operator to dump data from sensitive tables.
In this lab, the database contains a table named `users` with columns `username` and `password`.

---

##  Phase 1: Analysis

1.  **Column Count:** I confirmed the query returns **2 Columns**.
2.  **Type Check:** I confirmed **both columns** accept text data by sending:
    * `' UNION SELECT 'a', 'a'--` $\rightarrow$ **200 OK**.

---

##  Phase 2: Data Extraction

I constructed a query to map the database columns to the output columns:
* **Output Column 1** $\leftarrow$ `username`
* **Output Column 2** $\leftarrow$ `password`

### The Payload:
```sql
' UNION SELECT username, password FROM users--
```

## Execution Result:
The application displayed the product list, followed by the user credentials.

User: administrator

Password: [Extracted Password]

## Remediation
1. Ensure the database user has Least Privilege access (should not be able to read the users table from the products page query).

2. Use Parameterized Queries to prevent SQL injection entirely.