# Server-Side Request Forgery (SSRF)

**Category:** Web Security / Server-Side Injection  
**Focus:** PortSwigger Web Security Academy Labs  
**Status:** ✅ Completed

## Introduction
Server-Side Request Forgery (SSRF) is a web security vulnerability that allows an attacker to induce the server-side application to make requests to an unintended location.

In a typical SSRF attack, the attacker might cause the server to make a connection to internal-only services within the organization's infrastructure. In other cases, they may be able to force the server to connect to arbitrary external systems.

## Solved Labs & Techniques

### 1. Basic SSRF against the Local Server
**Objective:** Access the `/admin` panel (accessible only via localhost) and delete the user `carlos`.

* **Vulnerability:** The application takes a user-supplied URL (in the stock check API) and fetches data from it without validation.
* **Technique:** Modifying the `stockApi` parameter to request the loopback interface (`localhost`).
* **Payload:**
    ```http
    stockApi=http://localhost/admin/delete?username=carlos
    ```

### 2. Basic SSRF against another Backend System
**Objective:** Use the web server as a proxy to scan the internal network (`192.168.0.x`) to find an administrative interface on port `8080`.

* **Vulnerability:** The web server has access to a private internal network that is not accessible from the public internet.
* **Technique:** **Internal Network Scanning** using Burp Intruder. I iterate through the last octet of the IP address (1-255) to identify active internal services.
* **Payload (Intruder):**
    ```http
    stockApi=[http://192.168.0.](http://192.168.0.)§1§:8080/admin
    ```
* **Result:** Found the admin interface at `192.168.0.224` (IP varies by lab instance).

### 3. SSRF with Blacklist-based Input Filter
**Objective:** Bypass a "Blacklist" filter that blocks `127.0.0.1` and `admin` to delete user `carlos`.

* **Vulnerability:** Weak input validation that relies on blocking specific keywords rather than validating the structure.
* **Technique:** **Obfuscation & Double URL Encoding**.
    1.  **IP Bypass:** Using `127.1` (an alternative representation of `127.0.0.1`).
    2.  **String Bypass:** Double URL encoding the letter 'a' in `admin` (`%61` -> `%2561`) to confuse the WAF but be decoded correctly by the backend.
* **Payload:**
    ```http
    stockApi=[http://127.1/%2561dmin/delete?username=carlos](http://127.1/%2561dmin/delete?username=carlos)
    ```

### 4. SSRF with Whitelist-based Input Filter
**Objective:** Bypass a "Whitelist" filter that only allows URLs beginning with `stock.weliketoshop.net`.

* **Vulnerability:** Inconsistent URL parsing between the security filter and the HTTP client.
* **Technique:** **URL Parser Confusion** using Credential syntax (`@`) and Fragments (`#`).
    * `username@host` logic sends the request to the *host* while treating the first part as credentials.
    * `#` (Hash) is used to terminate the hostname for the backend, but i must **Double URL Encode** it (`%2523`) so the filter reads the allowed domain after it.
* **Payload:**
    ```http
    stockApi=http://localhost:80%2523@stock.weliketoshop.net/admin/delete?username=carlos
    ```
    * *Explanation:* The filter sees `stock.weliketoshop.net` (Valid). The backend executes `http://localhost:80` and ignores the rest as a fragment.

### 5. SSRF with Filter Bypass via Open Redirection
**Objective:** Exploit a strict whitelist by chaining the attack with an Open Redirect vulnerability found on the site.

* **Vulnerability:** The application trusts its own domain, but contains an endpoint (`/product/next`) that redirects users to any URL provided in the `path` parameter.
* **Technique:** **Vulnerability Chaining**. I ask the stock API to visit the internal "Next Product" link, which then redirects the server internally to the Admin Panel.
* **Payload:**
    ```http
    stockApi=/product/next?path=[http://192.168.0.12/admin/delete?username=carlos](http://192.168.0.12/admin/delete?username=carlos)
    ```

##  Prevention & Mitigation

To prevent SSRF vulnerabilities, developers should implement the following defenses:

1.  **Whitelist, Don't Blacklist:** Strictly validate user input against a rigorous whitelist of permitted domains or protocols.
2.  **Network Layer Defenses:** Ensure the web server is on a separate network segment and cannot talk to sensitive internal systems (like Admin panels or Databases) unless explicitly necessary.
3.  **Disable Redirections:** Configure the HTTP client used by the server to **not** automatically follow HTTP redirections.
4.  **Input Sanitization:** Verify that the input matches the expected URL structure (scheme, host, port, and path) before processing.