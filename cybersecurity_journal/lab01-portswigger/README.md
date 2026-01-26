# 🛡️ Lab Report: SQL Injection (Retrieval of Hidden Data)

| **Platform** | PortSwigger Web Security Academy |
| :--- | :--- |
| **Category** | SQL Injection (SQLi) |
| **Severity** | High / Critical |
| **Status** | ✅ Solved |
| **Date** | 27 Jan 2026 |

---

## 🎯 Objective
The goal of this lab is to display product details that are currently hidden (unreleased) by the application. The application filters products based on categories but uses an unsafe SQL query, allowing us to manipulate the `WHERE` clause.

---

## 🔍 Vulnerability Analysis
The application takes user input from the URL (`category` parameter) and concatenates it directly into the backend SQL query without validation.

**Vulnerable Backend Logic:**
```sql
SELECT * FROM products WHERE category = 'USER_INPUT' AND released = 1;
```
flaw: The query explicitly checks for released = 1 to show only public products. We need to bypass this check.

# Steps to Reproduce

Access the Lab: Open the application and click on the "Gifts" category filter.

Analyze URL: Observe the URL structure:

https://<LAB-ID>.web-security-academy.net/filter?category=Gifts

Inject Payload: Append the payload to the category parameter: .../filter?category=Gifts' OR 1=1--

Execute: Press Enter to send the request.

Verify: The page reloads and displays all products, including the unreleased ones.

``` sql
SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1;
' (Single Quote): Closes the data field for 'Gifts'.
 ```

OR 1=1:

        This is a "Tautology" (Always True).

        Since we used OR, the database checks: "Is the category Gifts? OR Is 1 equal to 1?"

        Because 1=1 is true, the entire condition becomes True for every row in the table.

-- (Double Dash):

            This is the SQL comment indicator.

            It forces the database to ignore the rest of the query (AND released = 1).

            This successfully removes the restriction on hidden products.

# Remediation (How to Fix)
To prevent this vulnerability, the developer should use Prepared Statements (Parameterized Queries). This ensures that user input is treated as data, not executable code.

Documented by: riyaz