#  DOM XSS in `innerHTML` Sink

##  Lab Description
This lab demonstrates a DOM-based Cross-Site Scripting (XSS) vulnerability. The application processes user input from the URL and inserts it into the page using the `innerHTML` property.

##  Objective
Perform a Cross-Site Scripting attack that calls the `alert` function. 

**Constraint:** The `innerHTML` sink prevents standard `<script>` tags from executing, so an alternative vector is required.

##  Vulnerability Analysis
* **Source:** `window.location.search` (The URL query parameter).
* **Sink:** `element.innerHTML` (Inserts HTML content into an element).
* **The Restriction:** HTML5 specifications state that `<script>` tags inserted via `innerHTML` should not be executed by the browser.

##  The Exploit (Payload)

Since `<script>` tags are blocked, i use an HTML Event Handler on an image tag.

```html
<img src=x onerror=alert(1)>
```
## How it works:
1. Injection: The payload is inserted into the DOM.

2. Rendering: The browser renders the <img> tag.

3. Error Trigger: The browser attempts to load the image from src=x. Since "x" is not a valid image URL, it fails.

4. Execution: The failure triggers the onerror event, which executes the JavaScript alert(1).

## Reproduction Steps
1. Open the vulnerable lab page.

2. Locate the search bar or manipulate the URL parameter directly.

3. Inject the payload into the search parameter: ?search=<img src=x onerror=alert(1)>

4. Press Enter/Search.

5. Observe the alert popup.