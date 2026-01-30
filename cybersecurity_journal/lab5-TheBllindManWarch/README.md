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

In this scenario, we inject a query that forces the database to **"Sleep" (Pause)** for a specific duration if our condition is TRUE. By measuring the time taken for the server to respond, we can infer information.

* **Rule:** If Response Time $\ge$ 10 seconds $\rightarrow$ Condition is **TRUE**.
* **Rule:** If Response Time is Instant $\rightarrow$ Condition is **FALSE**.

---

## Phase 1: Database Fingerprinting

Since the application suppresses errors, we first had to identify the database type by testing different "sleep" commands.

### The Test Vectors:
* **Oracle:** `dbms_pipe.receive_message(('a'),10)`
* **Microsoft:** `WAITFOR DELAY '0:0:10'`
* **PostgreSQL:** `pg_sleep(10)` $\leftarrow$ **(Confirmed)**

**Injection Point:** `TrackingId` Cookie.

**Successful Payload:**
```sql
'||pg_sleep(10)--
```