# Distributed Systems, Cloud, Testing, and DevOps

## Executive Summary

Once a system crosses process, machine, or team boundaries, the primary problem becomes coordination under partial failure. Cloud and DevOps are operational enablers; they do not remove distributed-systems complexity.

## Complete Explanation

### Distributed Systems

- Expect latency, retries, duplication, reordering, and partial failure.
- Core design topics: consistency, availability, partition handling, idempotency, backpressure, and observability.

### Cloud

- Cloud provides managed primitives, not free architecture.
- Important mental models: stateless compute, durable storage, IAM, networking, autoscaling, and cost observability.

### Testing

- Unit tests verify local logic.
- Integration tests verify boundaries.
- End-to-end tests verify user-critical flows.
- Production verification needs metrics, traces, alerts, and rollback plans.

### DevOps

- CI/CD shortens feedback loops.
- Good pipelines enforce build reproducibility, tests, artifacts, and deployment discipline.
- Containers help packaging consistency but do not guarantee good deployment practice.

## Common Errors

- Designing for scale before designing for correctness.
- Overusing microservices.
- Treating containers as security boundaries.
- Having tests with no production observability.

## References

- Docker docs: https://docs.docker.com/
- Docker overview: https://docs.docker.com/get-started/docker-overview/
