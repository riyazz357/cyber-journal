# 1st lab

#  Lab: JWT authentication bypass via unverified signature
**Platform:** PortSwigger Web Security Academy
**Goal:** Modify the JWT session cookie to access the admin panel and delete user `carlos`.
**Vulnerability:** Insecure JWT Implementation (The server decodes the payload but completely fails to verify the signature cryptographically).

##  Prerequisites (The Pro Tool)
To avoid manual Base64URL encoding errors (like padding `=` or accidental spaces), use the **JWT Editor** extension.
1. In Burp Suite, go to **Extensions -> BApp Store**.
2. Search for **JWT Editor** and click **Install**.

[Image of Burp Suite JWT Editor extension modifying payload claims]

## Step-by-Step Exploitation

### Step 1: Capture the Session Token
1. Log in to the application using the given credentials (`wiener:peter`).
2. Go to Burp Suite's **HTTP History** and find the `GET /my-account` request.
3. Right-click the request and select **Send to Repeater (Ctrl+R)**.

### Step 2: Forge the JWT Payload
1. Go to the **Repeater** tab.
2. On the right side panel (Inspector/Message Editor), look for the newly added **JSON Web Token** tab.
3. Expand the **Payload** section. You will see the user claims, including `"sub": "wiener"`.
4. Change the value of `"sub"` to `"administrator"`.
5. **Crucial:** Click the **Apply changes** button at the bottom of the JWT panel. Burp will automatically re-encode the payload safely into the `Cookie` header without messing up the formatting or signature.

### Step 3: The Takedown (Access Admin & Delete)
1. In the same Repeater request, change the top request line from `GET /my-account HTTP/2` to **`GET /admin HTTP/2`**.
2. Click **Send**. You should get a `200 OK` response, confirming you are now an Admin.
3. To finish the lab, change the request line again to **`GET /admin/delete?username=carlos HTTP/2`**.
4. Click **Send**. The lab will be marked as solved! 🎉

---
**Key Takeaway:** Never trust client-provided data. Even if a JWT looks valid, the backend MUST verify the signature using the server's secret key before trusting the claims inside the payload.