# Databases, APIs, Backend, Frontend, and Mobile

## Executive Summary

Application engineering is boundary engineering. Databases manage durable state. APIs expose contracts. Backend coordinates policy and side effects. Frontend manages user intent and rendering. Mobile adds constrained runtime, lifecycle, and platform-specific architecture.

## Complete Explanation

### Databases

- SQL systems prioritize relational modeling, transactions, and expressive queries.
- NoSQL systems optimize for different access patterns, scale models, or schema flexibility.
- PostgreSQL is a strong default when the domain is not yet fully known.

### APIs

- A good API has clear resource semantics, errors, idempotency, authentication, and versioning strategy.
- HTTP is not just transport; semantics matter.

### Backend

- Handles validation, orchestration, policy, persistence, async workflows, and observability.
- Main risks: hidden coupling, transaction leakage, and poor failure handling.

### Frontend

- Main concerns: state ownership, rendering model, network boundaries, accessibility, and performance.

### Mobile / Android / Kotlin / Java / Python

- Android requires lifecycle-aware architecture.
- Kotlin is the modern default for Android.
- Java remains central across enterprise ecosystems and the JVM.
- Python is highly productive for automation, data, backend glue, and AI tooling.

## References

- PostgreSQL docs and site: https://www.postgresql.org/
- Android development docs: https://developer.android.com/develop
- Android app fundamentals: https://developer.android.com/guide/components/fundamentals
- Kotlin docs: https://kotlinlang.org/docs/home.html
- Kotlin for Android learn page: https://developer.android.com/kotlin/learn
- Python docs: https://www.python.org/doc/
