# Lab: Reflected XSS into HTML context with nothing encoded

| **Category** | Web Security / Client-Side |
| :--- | :--- |
| **Vulnerability Type** | Reflected XSS (HTML Context) |
| **Goal** | Inject JavaScript to trigger an `alert(1)` popup. |
| **Difficulty** | 🟢 Apprentice |
| **Status** | ✅ Solved |

## Conceptual Overview
In a Reflected XSS attack, the application receives data in an HTTP request and includes that data within the immediate response in an unsafe way. Since the input is reflected directly into the HTML body without encoding, arbitrary HTML tags can be injected.

## Exploitation Steps

### Phase 1: Context Identification
Injected a probe string (`Hacker`) into the search bar.
Inspected the source code:
```html
<h1>0 search results for Hacker</h1>
```
The input lands directly between HTML tags.

## Phase 2: The Payload
Since there are no restrictions, i can simply open a new <script> tag.

Payload:

```HTML
<script>alert(1)</script>
```
## Execution Result
The browser parsed the script tag and executed the JavaScript, displaying the alert popup.