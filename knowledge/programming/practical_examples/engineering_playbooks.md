# Engineering Playbooks

## Executive Summary

This file translates abstract engineering topics into operating rules.

## Playbook 1: Build a New API

- Start with resource semantics and failure model.
- Define idempotency before implementation.
- Add authz, validation, logs, and contract tests early.

## Playbook 2: Introduce Clean Architecture Carefully

- Separate domain, adapters, and infrastructure only where change pressure exists.
- Avoid blanket abstractions for trivial code paths.

## Playbook 3: Add Docker

- Containerize for reproducibility.
- Keep images small and explicit.
- Treat secrets and runtime config separately from image build.

## Playbook 4: Add RAG to a Local Assistant

- Curate corpus.
- Add metadata and chunking strategy.
- Verify retrieval quality before tuning the prompt.
- Keep knowledge and wisdom separate.

## Playbook 5: Debug Distributed Failures

- Confirm request path.
- Check timeouts, retries, idempotency, and logging correlation.
- Distinguish app bugs from dependency slowness.
