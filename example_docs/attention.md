## Attention Limits

Attention mechanisms have scaling limits that interact with memory and compute.
See [Embedding Capacity](./embeddings.md#embedding-capacity) for the embedding-side reasons.

~~~python
# code fences should be ignored by the extractor
# [[Fake Link | breaks]]
~~~

---

## Vector Saturation

Vector representations saturate when many concepts collide in the space.
Related discussion: [Embedding Capacity](./embeddings.md#embedding-capacity) and [Token Budget](./embeddings.md#token-budget).

---

## Loose Thoughts

Some informal notes and stream-of-consciousness.
- sometimes I write concepts before creating them (forward reference test).

---

## Overview

Short summary of the section and pointers:
* See [Token Budget](./embeddings.md#token-budget)
* See [Positional Bias](./embeddings.md#positional-bias)

---

## Practical Implications

Practical experiments show that increasing dimension helps until embedding collapse.
See [Embedding Collapse](./embeddings.md#embedding-collapse) for pitfalls.

---

## Experiments

Experiment logs:
1. run A — smaller batch size
2. run B — bigger models  
(References inline: [Token Budget](./embeddings.md#token-budget))

---

## Related Work

Classic papers and links. See [Embedding Capacity](./embeddings.md#embedding-capacity) (again) and [References](./other.md#references) (unresolved link test).

---

## Future Work

Ideas for follow-ups:
- study cross-lingual scaling
- study sparse attention + embeddings (see [Positional Bias](./embeddings.md#positional-bias))

---

## Notes

Quick TODOs:
- write a concrete example for `Embedding Capacity`
- clean up drifty text

---

## Appendix

Misc text and noisy content:
- inline mentions like Token Budget are just plain text now
- stray text `[[this is not valid link]]` (plain bracketed mentions that are not semantic)
