# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅ Yes     |

## Reporting a Vulnerability

If you discover a security vulnerability in **agent-converter**, please **do not** open a public GitHub issue.

Instead, email the maintainers privately:

- **Email:** security@example.com
- **Subject line:** `[agent-converter] Security vulnerability`

Please include:
1. A description of the vulnerability.
2. Steps to reproduce (if applicable).
3. Potential impact.
4. Your suggested fix (optional but welcome).

You can expect an acknowledgment within **48 hours** and a full response within **7 days**.

## Scope

agent-converter is a pure-Python, zero-dependency library that performs data type conversion.
It does **not** make network requests, execute arbitrary code, or read/write to the filesystem.
The attack surface is limited to maliciously crafted input strings — please report any cases
where such input can cause unexpected behaviour (crashes, excessive memory/CPU consumption, etc.).
