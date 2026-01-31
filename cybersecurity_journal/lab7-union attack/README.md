# Lab: SQL Injection UNION Attack (Determining Column Count)

| **Category** | Web Security / SQL Injection |
| :--- | :--- |
| **Vulnerability Type** | UNION-Based SQLi |
| **Goal** | Determine the number of columns returned by the query. |
| **Tools Used** | Burp Suite (Repeater) / Browser URL |
| **Status** | ✅ Solved |

---

## Conceptual Overview

**UNION-Based SQL Injection** allows an attacker to retrieve data from other tables in the database by combining the results of the original query with the results of an injected query.

However, for a `UNION` operator to work, two strict conditions must be met:
1.  **Same Number of Columns:** The injected query must have the same number of columns as the original query.
2.  **Compatible Data Types:** The data types in each column must be compatible between the two queries.

Before extracting any data, i must first enumerate the number of columns used by the backend query.

---

##  Phase 1: Column Enumeration (The `ORDER BY` Method)

I used the `ORDER BY` clause to guess the number of columns. This clause forces the database to sort the result by a specific column index. If i try to sort by a column that doesn't exist, the database throws an error.

**Injection Point:** `category` parameter in the URL.

### The Process:
1.  `' ORDER BY 1--` $\rightarrow$ **200 OK** (Column 1 exists).
2.  `' ORDER BY 2--` $\rightarrow$ **200 OK** (Column 2 exists).
3.  `' ORDER BY 3--` $\rightarrow$ **200 OK** (Column 3 exists).
4.  `' ORDER BY 4--` $\rightarrow$ **500 Internal Server Error** 💥.

**Conclusion:** Since sorting by column 4 failed, the query returns **3 Columns**.

---

##  Phase 2: Payload Verification (The `NULL` Method)

Once i determined there were 3 columns, i needed to create a valid `UNION` payload to solve the lab. i used `NULL` values because `NULL` is compatible with every data type (String, Integer, Date, etc.), avoiding type-mismatch errors.

### The Winning Payload:
i appended the following to the URL:

```sql
' UNION SELECT NULL,NULL,NULL--
```
### Breakdown:
UNION: Joins our query with the original.

SELECT: Starts our injected query.

NULL,NULL,NULL: Represents 3 empty columns to match the original query's structure.

--: Comments out the rest of the original query.

**Result**: The application loaded successfully without errors, confirming the structure match.

## Remediation
1. Parameterized Queries: Use Prepared Statements to ensure user input is never interpreted as SQL commands.

2. Input Validation: Sanitize input to reject SQL keywords (like UNION, ORDER BY) if they are not expected.

3. Least Privilege: Ensure the database user used by the application only has access to the tables it strictly needs, preventing access to sensitive tables via UNION attacks.

## Documented By:*Riyaz*