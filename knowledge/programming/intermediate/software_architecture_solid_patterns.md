# Software Architecture, Clean Architecture, SOLID, and Design Patterns

## Executive Summary

Architecture is about controlling change, coupling, and failure propagation. SOLID and design patterns are means, not goals. Use them when they reduce complexity and sharpen boundaries, not as ceremonial decoration.

## Complete Explanation

### Fundamentals

- Architecture defines component boundaries, dependencies, interfaces, and runtime interactions.
- Clean Architecture emphasizes policy vs detail separation and inward dependency flow.
- SOLID offers heuristics for maintainable object-oriented design.

### Intermediate Concepts

- Patterns like Strategy, Adapter, Factory, Observer, and Repository solve recurring structural problems.
- Dependency inversion is most useful at unstable boundaries: storage, transport, vendors, frameworks.
- Bounded contexts and explicit contracts matter more than class hierarchies in larger systems.

### Advanced Concepts

- Over-abstraction creates accidental complexity.
- A simple modular monolith often beats a premature distributed system.
- Architecture should optimize for dominant change vectors, not for hypothetical future scale.

## Best Practices

- Isolate framework concerns.
- Keep domain logic testable without network or database.
- Prefer explicit data flow over hidden magic.

## Common Errors

- Using patterns because a book named them.
- Confusing interface count with architectural quality.
- Splitting services before the domain is understood.

## References

- RFC 9110 for API semantics baseline: https://www.rfc-editor.org/info/rfc9110/
- Android app fundamentals for component thinking: https://developer.android.com/guide/components/fundamentals
