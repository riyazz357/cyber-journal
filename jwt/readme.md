# Comprehensive Technical Guide to

# JSON Web Tokens (JWT): Architecture,

# Exploitation, and Defensive Engineering

## 1. Architectural Overview of JSON Web Tokens

A JSON Web Token (JWT), standardized under RFC 7519, is an open, industry-standard
method for representing claims securely between two parties. In modern web development,
particularly within distributed microservice architectures and RESTful APIs, JWTs serve as a
primary mechanism for stateless authentication and authorization.
Unlike traditional session-based authentication—where the server maintains a stateful
record of active sessions in a database or memory store—JWTs encapsulate all necessary
user routing and privilege data directly within the token. The server relies entirely on
cryptographic verification to trust the token's contents, eliminating the need for backend
session lookups and allowing systems to scale horizontally with ease.

## 2. Token Anatomy and Cryptographic Structure

A JWT is transmitted as a single, compact string comprised of three distinct segments,
delimited by periods (.). To ensure safe transmission across HTTP headers and URIs, each
segment is independently encoded using **Base64URL** encoding (which omits the +, /, and =
characters found in standard Base64).
**Structural Format:** [Header].[Payload].[Signature]

### 2.1 The JOSE Header

The JSON Object Signing and Encryption (JOSE) header dictates the metadata and the
cryptographic algorithms applied to the token.
JSON

1. {
2. "alg": "HS256",
3. "typ": "JWT"
4. }
● **alg (Algorithm):** Specifies the algorithm used for the signature (e.g., HS256 for
    HMAC with SHA-256, RS256 for RSA with SHA-256).
● **typ (Type):** Denotes the media type, typically "JWT".


```
● Advanced headers may also include kid (Key ID), jwk (JSON Web Key), or jku (JWK
Set URL) to assist the server in locating the correct verification key.
```
### 2.2 The Payload (Claims)

The payload contains the assertions, or "claims," regarding the authenticated entity. Claims
are divided into three categories:

1. **Registered Claims:** Standardized claims defined by IANA to ensure interoperability.
    ○ sub (Subject): The principal subject of the token (often the User ID).
    ○ exp (Expiration Time): The timestamp after which the token is invalid.
    ○ iat (Issued At): The timestamp of token generation.
    ○ iss (Issuer): The entity that generated the token.
2. **Public Claims:** Custom claims defined by developers, registered to avoid collisions.
3. **Private Claims:** Custom claims utilized for specific internal application logic (e.g.,
    "role": "administrator", "department": "finance").
**Security Imperative:** The payload is merely encoded, not encrypted.
Confidential or sensitive data (such as passwords, internal IP addresses, or
financial information) must never be stored within a standard JWT payload.

### 2.3 The Cryptographic Signature

The signature is the critical component that ensures data integrity and authenticity. It
prevents threat actors from tampering with the payload. The signature is computed by
applying the designated alg to the concatenated, encoded header and payload, utilizing a
cryptographic secret or private key.
Plaintext

5. // Signature Generation Process
6. HMACSHA256(
7. base64UrlEncode(header) + "." + base64UrlEncode(payload),
8. secret_key
9. )

## 3. The Authentication Lifecycle

1. **Authentication:** The client submits valid credentials (e.g., username and password)
    to the Identity Provider (IdP) or authentication server.
2. **Generation & Signing:** The server validates the credentials, constructs the JWT
    header and payload, and signs the token using its cryptographic key.
3. **Issuance:** The server transmits the signed JWT back to the client.
4. **Client Storage:** The client stores the token (optimally within an HttpOnly, Secure
    cookie to mitigate client-side extraction).


5. **Authorization Request:** For subsequent protected requests, the client includes the
    token, typically in the HTTP Authorization header utilizing the Bearer schema
    (Authorization: Bearer <token>).
6. **Stateless Verification:** The receiving server intercepts the request, mathematically
    validates the signature using its key, parses the claims, and grants or denies access
    based on the payload data—all without querying a database.

## 4. Advanced Exploitation Vectors and Methodologies

Vulnerabilities within JWT implementations rarely stem from the cryptographic algorithms
themselves, but rather from flawed implementation logic, improper input validation, and
misconfigured parsing libraries on the backend.

### 4.1 Unverified Signature Bypass

```
● Vulnerability Overview: The application decodes the Base64URL payload to
execute authorization logic but fails to invoke the cryptographic signature validation
routine. The server blindly trusts the decoded claims.
● Exploitation Methodology:
```
1. Capture a valid JWT assigned to a low-privileged user.
2. Isolate and decode the Payload segment.
3. Modify the privilege claims (e.g., alter "sub": "user" to "sub": "admin").
4. Base64URL-encode the manipulated payload.
5. Replace the original payload in the JWT string. The original signature is left
    intact.
6. Transmit the forged token. The server processes the elevated claims without
    validating the mismatched signature.

### 4.2 Flawed Signature Verification (alg: none)

```
● Vulnerability Overview: The JWT specification includes a none algorithm, originally
intended for contexts where token integrity is verified via other means (e.g., mutual
TLS). If a backend dynamically trusts the alg header supplied by the client rather
than enforcing a hardcoded algorithm, it can be bypassed.
● Exploitation Methodology:
```
1. Intercept the target JWT.
2. Decode and modify the Payload to elevate privileges.
3. Decode the Header and change the algorithm parameter: {"alg": "none"}.
4. Strip the cryptographic signature entirely from the token, leaving only the
    trailing delimiter (Header.Payload.).
5. The parsing library reads the none directive, skips the mathematical
    validation, and processes the forged token as fully authenticated.

### 4.3 Offline Cryptographic Brute Force (Weak Keys)


```
● Vulnerability Overview: Symmetric encryption (HS256) relies entirely on the entropy
and complexity of the shared secret key. If developers utilize low-entropy,
dictionary-based secrets (e.g., secret123, password), the signature can be
mathematically cracked offline.
● Exploitation Methodology:
```
1. Capture a single valid JWT from the target application.
2. Utilize high-performance hardware and a dictionary hashing utility (such as
    Hashcat) to execute an offline brute-force attack against the token's
    signature.
       ■ _Example Command:_ hashcat -a 0 -m 16500 target_jwt.txt wordlist.txt
3. Upon recovering the plaintext secret key, the threat actor can locally generate
    new tokens, assign arbitrary high-level privileges, and cryptographically sign
    them. The server will implicitly trust these perfectly forged tokens.

### 4.4 JWK Parameter Injection (Rogue Key Attack)

```
● Vulnerability Overview: In Asymmetric encryption (RS256), the jwk (JSON Web
Key) header parameter allows the token to embed the public key required for
verification. If the server fails to validate this key against a trusted internal keystore, it
will dynamically utilize the client-supplied key to verify the token.
● Exploitation Methodology:
```
1. The threat actor generates a rogue RSA Private/Public key pair locally.
2. The target JWT payload is modified to reflect administrative privileges.
3. The rogue Public Key is injected into the jwk header of the token.
4. The token is signed using the rogue Private Key.
5. Upon receipt, the vulnerable server extracts the attacker's public key from the
    header and uses it to verify the signature. Because the attacker signed it with
    the corresponding private key, the validation passes.

### 4.5 JKU Parameter Server-Side Request Forgery (SSRF)

```
● Vulnerability Overview: The jku (JWK Set URL) header specifies a URI from which
the server should dynamically retrieve the public verification key. Failure to enforce
strict URI whitelisting allows an attacker to control the retrieval destination, resulting
in an SSRF.
● Exploitation Methodology:
```
1. The threat actor generates an RSA key pair and hosts the Public Key (in JWK
    format) on an external, attacker-controlled web server.
2. The JWT payload is altered for privilege escalation.
3. The attacker injects the external URI into the jku header (e.g., "jku":
    "https://malicious-server.com/keys.json").
4. The token is signed with the attacker's Private Key.
5. The target server parses the header, initiates an outbound HTTP request to
    the malicious server to fetch the key, and subsequently uses it to validate the
    forged token.


### 4.6 Key ID (kid) Directory Traversal

```
● Vulnerability Overview: The kid header acts as a pointer, instructing the server
which specific key to retrieve from its local filesystem or database. Improper
sanitization of this parameter introduces critical directory traversal vulnerabilities.
● Exploitation Methodology:
```
1. The threat actor injects a traversal payload into the kid header, targeting a
    predictably empty file (e.g., /dev/null on Linux systems): "kid":
    "../../../../../../../dev/null".
2. The backend filesystem reads /dev/null, returning a Null byte stream (zero
    bytes). The application inadvertently utilizes this empty stream as the
    symmetric secret key.
3. The attacker alters the token payload to gain administrative access.
4. The attacker locally signs the forged token using an encoded Null Byte
    (represented as "AA==" in Base64).
5. The server compares the Null Byte key from its filesystem against the
    attacker's Null Byte signature, resulting in a successful cryptographic match.

### 4.7 Key ID (kid) Injection (SQLi / CMDi)

```
● Vulnerability Overview: If the backend utilizes the kid parameter to dynamically
query a database for the secret key, or passes it into a system command without
parameterization, it opens the system to standard injection vectors.
● Exploitation Methodology:
○ SQL Injection: Injecting "kid": "key1' OR 1=1--" can manipulate the database
into returning a predictable, known key, allowing the attacker to sign tokens
using that known key.
○ Command Injection: Injecting "kid": "key1; whoami #" allows the attacker to
execute arbitrary shell commands on the backend infrastructure hosting the
authentication service.
```
## 5. Enterprise-Grade Defensive Architecture

To engineer a resilient JWT authentication infrastructure and mitigate the aforementioned
exploitation vectors, the following security controls must be strictly enforced at the
architectural level:

1. **Strict Cryptographic Whitelisting:** Backend services must explicitly define and
    enforce acceptable cryptographic algorithms within their JWT libraries (e.g.,
    algorithms: ['RS256']). The application must systematically reject the alg: none
    directive unconditionally in all production environments.
2. **High-Entropy Secret Management:** For symmetric implementations (HS256),
    secret keys must be generated using Cryptographically Secure Pseudorandom
    Number Generators (CSPRNG), maintaining a minimum length of 256 bits (
    bytes). Keys must never be derived from dictionary words and should be rotated
    periodically.


3. **Deprecate Client-Supplied Cryptography:** Backend logic must completely ignore
    jwk, jku, and x5c headers provided by the client. Signature verification must rely
    exclusively on internally managed, hardcoded public keys or enterprise Key
    Management Services (e.g., AWS KMS, HashiCorp Vault, Azure Key Vault).
4. **Input Sanitization and Validation:** Treat all header parameters, specifically the kid,
    as highly untrusted user input. The kid must be validated against a strict, predefined
    allowlist of known Key IDs. Direct mapping of the kid parameter to filesystem paths or
    dynamic SQL queries must be strictly prohibited to prevent Traversal and Injection
    attacks.
5. **Secure Token Persistence:** To mitigate Cross-Site Scripting (XSS) token extraction,
    JWTs should be stored client-side utilizing HttpOnly, Secure, and SameSite=Strict
    cookie attributes. Storing tokens in HTML5 localStorage or sessionStorage exposes
    them to JavaScript-based theft.
6. **Granular Expiration and Revocation:** Access tokens must maintain a short
    time-to-live (TTL), typically 10 to 15 minutes. To facilitate session termination prior to
    natural expiration, a robust revocation architecture must be implemented utilizing a
    distributed, high-performance Token Blacklist (e.g., Redis) to track and reject
    invalidated token IDs (jti).
7. **Mandatory Verification Checks:** Ensure that the authentication middleware
    explicitly invokes the signature verification function before any payload decoding or
    business logic routing occurs. Code paths that allow parsing without prior validation
    must be eliminated.
    DOCUMENTED BY: MOHAMMAD RIYAZ


