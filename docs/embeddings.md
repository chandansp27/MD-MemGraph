# Embedding Capacity

Embeddings compress high-dimensional signals. There is a finite capacity per vector.
This section [[supports]] the attention-side observations (see [[../docs/attention.md#Attention Limits | related]]).

---

## Token Budget

Token budget constraints affect model context and embeddings.
Links: [[../docs/attention.md::Attention Limits | related]], [[Vector Saturation | related]].

---

## Positional Bias

Position encodings interact with embeddings in subtle ways.
Example: see [[../docs/attention.md#Practical Implications | related]].

---

## Embedding Collapse

When vectors collapse, nearest neighbors become meaningless.
Countermeasures: regularization and orthogonalization.
See [[Embedding Capacity | supports]] and [[Optimization | helps]].

---

## Dimensionality

Higher dimensions increase capacity but cost compute.
See [[Embedding Capacity | supports]].

---

## Optimization

Local optimization tweaks (LR schedules, warmup).
This links to tests in [[Experiments | related]].

---

## Benchmarks

Benchmark notes and references.
Compare with attention experiments stored in [[../docs/attention.md#Experiments | related]].

---

## Applications

Where embeddings are used:
- search
- retrieval-augmented generation
Edge-case: token budget trade-offs -> [[Token Budget | related]].

---

## Limitations

Practical limits: representational interference and dataset bias.
See [[Nonexistent Concept | mentions]] (forward ref intentionally left unresolved).

---

## Appendix

Small utilities and logs:
~~~text
# should be ignored
[[Ignore This | breaks]]
~~~
