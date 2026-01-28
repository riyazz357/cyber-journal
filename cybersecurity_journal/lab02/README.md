# Lab Report: SQL Injection with Filter Bypass via XML Encoding

| **Platform** | PortSwigger Web Security Academy |
| :--- | :--- |
| **Category** | SQL Injection (SQLi) |
| **Technique** | XML Entity Encoding / WAF Bypass |
| **Severity** | Critical |
| **Status** | ✅ Solved |

---

##  Objective
The goal is to perform a SQL Injection attack on an application that uses XML for data transmission. The application is protected by a Web Application Firewall (WAF) that blocks malicious keywords like `UNION` and `SELECT`. We must bypass this filter to retrieve the administrator's password.

---

## Vulnerability Analysis
The application's "Check Stock" feature transmits data in XML format.
* **Input Vector:** The `storeId` parameter within the XML body.
* **Defense Mechanism:** A WAF blocks requests containing standard SQL keywords.
* **The Flaw:** The WAF inspects the raw XML input, but the application's XML parser decodes HTML/XML entities *before* passing the data to the database.

**The Bypass Logic:**
By encoding the SQL payload into XML entities (e.g., `S` becomes `&#x53;`), the payload passes through the WAF as "safe text" but is reconstructed into a malicious SQL query by the XML parser.

---

##  The Attack (Payload)

**1. Target Query (Oracle DB):**
We want to extract usernames and passwords from the `users` table.
```sql
1 UNION SELECT username || ':' || password FROM users
```

## Steps to Reproduce
md

1. Intercept Request: Use Burp Suite to intercept the "Check Stock" request.

2. Send to Repeater: Move the request to the Repeater tab for modification.

3. Insert Payload: inside the <storeId> tag, place the raw SQL payload: 1 UNION SELECT username || ':' || password FROM users

4. Encode: Select the payload text within Burp, right-click, and choose Convert selection > HTML > HTML encode all characters.

5. Execute: Send the request.

6. Retrieve Data: The response will contain the administrator's credentials (e.g., administrator:password123).

7. Login: Use the credentials to log in as the administrator.

## Technical Breakdown (The Journey)

1. Hacker sends: &#x55;... (Encoded Payload).

2. WAF Checks: Does &#x55;... match the blacklist ("UNION")? No. -> PASS.

3. XML Parser: Receives &#x55;.... Decodes it to "UNION". -> PASS.

4. Database: Receives SELECT ... UNION .... Executes the query. -> HACKED

# Remediation (How to Fix)
1. Input Validation: Validate input after XML decoding, not just before.

2. Parameterized Queries: Always use Prepared Statements so that even decoded SQL is treated as data, not code.

3. Patch WAF: Configure the WAF to decode XML/HTML entities before inspecting for malicious keywords.

Documented by: Riyaz