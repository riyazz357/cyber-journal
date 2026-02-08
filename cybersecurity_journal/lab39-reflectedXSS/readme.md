```markdown
# Lab: Reflected XSS into HTML context with most tags and attributes blocked

| **Category** | Web Security / Client-Side |
| :--- | :--- |
| **Vulnerability Type** | Reflected XSS (WAF Bypass) |
| **Goal** | Bypass a whitelist/WAF to execute XSS automatically. |
| **Difficulty** | 🔴 Hard |
| **Status** | ✅ Solved |

## Conceptual Overview
When an application uses a Web Application Firewall (WAF) to block common tags (like `<script>`, `<img>`) and events, attackers must fuzz the application to identify allowed permutations of tags and events.

## Exploitation Steps

### Phase 1: Fuzzing (Burp Intruder)
1.  **Tags:** Fuzzed all HTML tags. Found `<body>` was allowed (200 OK).
2.  **Events:** Fuzzed events on the body tag. Found `onresize` was allowed.

### Phase 2: The Exploit (Iframe Automation)
Since `onresize` requires user interaction (window resizing), i automated this using an `iframe` on an exploit server.

**Exploit Server Payload:**
```html
<iframe src="[https://TARGET-LAB-ID.web-security-academy.net/?search=%3Cbody+onresize%3Dprint%28%29%3E](https://TARGET-LAB-ID.web-security-academy.net/?search=%3Cbody+onresize%3Dprint%28%29%3E)" onload=this.style.width='100px'></iframe>
```
## Execution Result
1. Victim visits exploit page.

2. Iframe loads the target search with the payload.

3. onload changes iframe width.

4. onresize triggers on the target.

5. print() executes.