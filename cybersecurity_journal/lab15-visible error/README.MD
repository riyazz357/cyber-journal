# Lab: Visible Error-Based SQL Injection

| **Category** | Web Security / SQL Injection |
| :--- | :--- |
| **Vulnerability Type** | Error-Based SQLi |
| **Goal** | Extract the administrator password via verbose error messages. |
| **Tools Used** | Burp Suite (Repeater) |
| **Status** | ✅ Solved |

---

## Conceptual Overview
When an application is configured to display verbose error messages (e.g., for debugging), attackers can intentionally cause a database error that "leaks" sensitive data within the error text.
* **The Technique (CAST Injection):** We force the database to convert a string (like a password) into an Integer. Since this is impossible, the database throws an error stating: *"Invalid input syntax for integer: 'THE_PASSWORD'"*.



---

## Exploitation Steps

### Phase 1: Triggering the Error
I identified that the `TrackingId` cookie was vulnerable. I injected a `CAST` function to convert the password into an integer.

### Phase 2: Handling Truncation
The server had a character limit on the cookie value. To prevent the query from being cut off (truncated), i removed the original Tracking ID value to save space.

### Phase 3: The Final Payload
I injected the following into the `TrackingId` cookie:

```sql
TrackingId=' AND 1=CAST((SELECT password FROM users LIMIT 1) AS INT)--
```
1. ': Closes the empty string literal.

2. CAST(... AS INT): Forces the type conversion error.

3. LIMIT 1: Ensures we only fetch one record to avoid "more than one row returned" errors.

## Execution Result:
The server responded with:

ERROR: invalid input syntax for integer: "[EXTRACTED_PASSWORD]"

I successfully extracted the password from the error string.