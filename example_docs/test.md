## Practical Tips

Short pragmatic tips for experiments. See [Token Budget](./embeddings.md#token-budget) and [Embedding Capacity](./embeddings.md#embedding-capacity).

---

## Implementation Notes

Notes on running the code: environment, seeds, and reproducibility.
Ref: [Optimization](./embeddings.md#optimization)

---

## Data Hygiene

Data cleaning tips. Occasionally references [Attention Limits](./attention.md#attention-limits) and [Vector Saturation](./attention.md#vector-saturation).

---

## Testing

Test designs and gold-standard checks.
Plan: unit tests that validate graph extraction (see [Experiments](./attention.md#experiments)).

---

## Integration

How to integrate the KG into the agent pipeline.
Example: agent sees `EDGE src=... rel=... dst=...` lines.

---

## Nonexistent Concept

This is intentionally left as a placeholder to test unresolved link handling:
[Nonexistent External Concept](./other.md#nonexistent-external-concept)

---

## References

Short bibliography pointers and cross-file pointers.
Also references: [Benchmarks](./embeddings.md#benchmarks)

---

## Changelog

- v0.1 initial notes
- v0.2 minor edits (see [Practical Tips](#practical-tips))

---

## Examples

Short runnable example (should be ignored if in code fence):

~~~python
# Example code:
def foo():
    # [[InlineFake | ignore]]
    return "ok"
~~~

Then outside fence: [Practical Tips](#practical-tips)

---

## Summary

Conclusions and next steps:
- write full draft about Embedding Capacity
- resolve [Nonexistent External Concept](./other.md#nonexistent-external-concept)
