# AI, Machine Learning, LLMs, Agents, RAG, and Vector Search

## Executive Summary

Modern AI systems are layered systems: models, prompts, retrieval, tools, evaluation, and runtime constraints. LLM applications fail less from lack of model intelligence than from poor context management, weak retrieval, hidden assumptions, and missing evaluation loops.

## Complete Explanation

### Fundamentals

- Machine learning learns patterns from data.
- Transformers are the dominant architecture behind modern LLMs.
- Embeddings map content into vector space for semantic retrieval.

### Intermediate Concepts

- RAG combines a parametric model with external retrieved context.
- Agents add tool use, iterative planning, and environment interaction.
- Vector search enables approximate nearest-neighbor retrieval over embeddings.

### Advanced Concepts

- High-quality RAG depends on corpus quality, chunking, metadata, retrieval strategy, and answer grounding.
- Agents need bounded tools, explicit state, failure handling, and evaluation.
- Small local models require ruthless prompt discipline and strong retrieval support.

## Best Practices

- Separate durable knowledge from operational memory.
- Keep source links and provenance.
- Evaluate retrieval quality separately from answer quality.
- Prefer narrow, reliable tools over vague autonomous behavior.

## Common Errors

- Stuffing huge prompts instead of improving retrieval.
- Treating embeddings as truth rather than a retrieval heuristic.
- Using agents where a deterministic workflow would be safer.

## Foundational References

- Transformer paper: https://arxiv.org/abs/1706.03762
- RAG paper: https://arxiv.org/abs/2005.11401
- ReAct paper: https://arxiv.org/abs/2210.03629
- Vector DB survey: https://arxiv.org/html/2402.01763v1
