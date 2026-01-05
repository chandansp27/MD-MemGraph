# Attention Limits

Attention mechanisms have scaling limits that interact with memory and compute.
See [[Embedding Capacity | supports]] for the embedding-side reasons.

~~~python
# code fences should be ignored by the extractor
# [[Fake Link | breaks]]
~~~

---

## Vector Saturation

Vector representations saturate when many concepts collide in the space.
Related discussion: [[Embedding Capacity | related]] and [[Token Budget | related]].

---

## Loose Thoughts

Some informal notes and stream-of-consciousness.
- sometimes I write [[Nonexistent Concept | mentions]] before creating it.

---

## Overview

Short summary of the section and pointers:
* See ../docs/embeddings.md#Token Budget
* See [[../docs/embeddings.md::Positional Bias | related]]

---

## Practical Implications

Practical experiments show that increasing dimension helps until embedding collapse.
See [[Embedding Collapse | related]] for pitfalls.

---

## Experiments

Experiment logs:
1. run A — smaller batch size
2. run B — bigger models  
(References inline: [[Token Budget | affects]])

---

## Related Work

Classic papers and links. See [[Embedding Capacity | supports]] (again) and [[../docs/other.md#References | references]].

---

## Future Work

Ideas for follow-ups:
- study cross-lingual scaling
- study sparse attention + embeddings (see [[Positional Bias | related]])

---

## Notes

Quick TODOs:
- write a concrete example for `Embedding Capacity`
- clean up drifty text

---

## Appendix

Misc text and noisy content:
- inline [[Token Budget]]
- stray text `[[this is not valid link]]` (plain bracketed mentions that are not semantic)
