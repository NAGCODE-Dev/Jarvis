# Networking, Linux, Git, and Security Foundations

## Executive Summary

Modern software lives on networks, runs on operating systems, changes through version control, and fails under security pressure unless designed carefully. These are not secondary skills; they are part of software correctness.

## Complete Explanation

### Networking

- HTTP semantics, methods, status codes, headers, caching, idempotency, and content negotiation matter at API boundaries.
- TCP/IP and DNS behavior shape latency, retries, and failure modes.

### Linux

- Processes, files, permissions, environment variables, signals, sockets, logs, and service management are baseline operational knowledge.

### Git

- Commits are immutable history units.
- Branching and merging manage concurrency in change.
- Small commits, readable diffs, and safe rollback matter more than clever rebasing rituals.

### Security

- Input handling, access control, secret management, transport security, dependency hygiene, and logging are continuous concerns.
- OWASP Top 10 is a baseline awareness document, not a complete security model.

## Common Errors

- Misusing HTTP verbs and caching.
- Treating Linux like a black box.
- Using Git history as a dump instead of an audit trail.
- Bolting security on after the architecture is already fixed.

## References

- HTTP Semantics RFC 9110: https://www.rfc-editor.org/info/rfc9110/
- Git docs: https://git-scm.com/docs
- Pro Git book: https://git-scm.com/book/en/v2
- OWASP Top 10 project: https://owasp.org/www-project-top-ten/
- OWASP Top 10 2025: https://owasp.org/Top10/2025/en/
