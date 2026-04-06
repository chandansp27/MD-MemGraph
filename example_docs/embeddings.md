## Embedding Capacity

Embeddings compress high-dimensional signals. There is a finite capacity per vector.
This section supports the attention-side observations (see [Attention Limits](./attention.md#attention-limits)).

---

## Token Budget

Token budget constraints affect model context and embeddings.
Links: [Attention Limits](./attention.md#attention-limits), [Vector Saturation](./attention.md#vector-saturation).

---

## Positional Bias

Position encodings interact with embeddings in subtle ways.
Example: see [Practical Implications](./attention.md#practical-implications).

---

## Embedding Collapse

When vectors collapse, nearest neighbors become meaningless.
Countermeasures: regularization and orthogonalization.
See [Embedding Capacity](#embedding-capacity) and [Optimization](#optimization).

---

## Dimensionality

Higher dimensions increase capacity but cost compute.
See [Embedding Capacity](#embedding-capacity).

---

## Optimization

Local optimization tweaks (LR schedules, warmup).
This links to tests in [Experiments](./attention.md#experiments).

---

## Benchmarks

Benchmark notes and references.
Compare with attention experiments stored in [Experiments](./attention.md#experiments).

---

## Applications

Where embeddings are used:
- search
- retrieval-augmented generation
Edge-case: token budget trade-offs -> [Token Budget](#token-budget).

---

## Limitations

Practical limits: representational interference and dataset bias.
See [Future Work](./attention.md#future-work) for follow-up ideas.

---

## Appendix

Small utilities and logs:
~~~text
# should be ignored
[[Ignore This | breaks]]
~~~
