## Knowledge Design

Principles and patterns for effectively structuring knowledge as a graph.

---

## Atomicity

### One Concept Per Block

The fundamental principle: Each block contains one atomic concept.

**Good**:
```markdown
## Backpropagation

Algorithm for computing gradients in neural networks.
Uses [Chain Rule](./math.md#chain-rule) for derivative computation.

---

## Gradient Descent

Optimization algorithm that uses gradients to minimize loss.
Computed by [Backpropagation](#backpropagation).
```

**Bad** (multiple concepts per block):
```markdown
## Training Algorithms

Backpropagation computes gradients using the chain rule.
Gradient descent uses those gradients to minimize loss.
Adam is a variant of gradient descent.
```

### Benefits of Atomicity

- **Findability**: Each concept has one clear location
- **Reusability**: Can link from multiple places
- **Maintainability**: Changes in one place only
- **Clarity**: Focused content easier to understand

### Determining Block Boundaries

Ask: "Can someone understand this concept in isolation?"

If the answer requires context from another section, split:
```markdown
## Backpropagation

[Background needed: Chain Rule](#chain-rule)

Algorithm explanation.

---

## Chain Rule

Mathematical foundation for backpropagation.
Used in: [Backpropagation](#backpropagation)
```

---

## Block Size

### Target Length

Aim for 2-5 sentences per block core concept:

```markdown
## Dense Layer

A fully-connected neural network layer where each neuron
connects to all inputs. Standard building block for feedforward
networks. Computationally simple but requires more parameters
than specialized layers.
```

Optional: Add examples or deeper explanation after separator.

### Too Long

```markdown
## Dense Layer

[50 lines of detailed explanation]
[Mathematical derivation]
[Implementation code]
[Performance analysis]
```

**Problem**: Hard to link meaningfully, violates atomicity

**Fix**: Split into separate concepts:
- Dense Layer (basic concept)
- Dense Layer Implementation (code)
- Dense Layer Performance (analysis)

### Too Short

```markdown
## Dense Layer

A fully-connected layer.

---
```

**Problem**: Lacks sufficient context

**Fix**: Expand to 2-3 sentences minimum:
```markdown
## Dense Layer

A fully-connected neural network layer where each neuron
connects to all inputs. Computationally efficient but requires
many parameters.
```

---

## Hierarchies and Levels

### Conceptual Hierarchy

Organize concepts from general to specific:

```
Level 1: Machine Learning (broad)
  ↓
Level 2: Supervised Learning (subset)
  ↓
Level 3: Classification (specific task)
  ↓
Level 4: Decision Trees (specific algorithm)
```

### Implementing Hierarchy

Use directory structure or explicit linking:

**Directory approach**:
```
docs/
  ├── fundamentals.md (Level 1 concepts)
  ├── intermediate.md (Level 2 concepts)
  └── advanced.md (Level 3+ concepts)
```

**Explicit linking approach**:
```markdown
## Hierarchy Guide

1. [Fundamentals](#fundamentals)
2. [Intermediate](#intermediate)
3. [Advanced](#advanced)
```

### Forward and Backward References

Link in both directions:

```markdown
## Classification (in fundamentals.md)

Specific task in [Machine Learning](./fundamentals.md#machine-learning).

---

## Machine Learning (in fundamentals.md)

Includes [Classification](#classification).
```

Both directions show the hierarchy.

---

## Organization Patterns

### By Domain

Group related concepts by subject area:

```
docs/
  ├── math/              # Mathematical foundations
  ├── ml-algorithms/    # ML algorithms
  ├── nlp/              # Natural language processing
  └── vision/           # Computer vision
```

Good for: Technical projects, specialized knowledge

### By Process

Organize by workflow or procedure:

```
docs/
  ├── data-preparation/
  ├── model-training/
  ├── evaluation/
  └── deployment/
```

Good for: How-to guides, processes, workflows

### By Audience

Different files for different levels:

```
docs/
  ├── beginner/        # Simplified concepts
  ├── intermediate/    # Deeper understanding
  └── advanced/        # Specialized topics
```

Good for: Educational content, learning paths

### Flat Structure

All concepts in single directory:

```
docs/
  ├── concept-a.md
  ├── concept-b.md
  ├── concept-c.md
  └── ...
```

Good for: Small graphs (< 50 concepts), flat knowledge

### Hybrid Approach

Combine multiple patterns:

```
docs/
  ├── overview.md              # Entry point
  ├── fundamentals/
  │   ├── concepts.md
  │   ├── math-foundations.md
  │   └── algorithms.md
  └── advanced/
      ├── specialist-a.md
      └── specialist-b.md
```

Good for: Large, complex knowledge bases (recommended)

---

## Cyclicity

### Acyclic Design (DAG)

Avoid cycles for clarity:

```
Prerequisites → Concepts → Applications
```

No concept points back up the chain.

**Benefits**:
- Clear learning progression
- Obvious dependency order
- Easier to understand structure

**Implementation**:
```markdown
## Foundations

Core concepts needed for [Intermediate](#intermediate).

---

## Intermediate

Builds on [Foundations](#foundations).
Required for [Advanced](#advanced).
```

One-directional flow.

### Allowing Cycles

Allow bidirectional relationships for balance:

```markdown
## Concept A

Related to [Concept B](#concept-b).

---

## Concept B

Related to [Concept A](#concept-a).
```

Both point to each other: A ↔ B

**Benefits**:
- Express real-world relationships
- Show mutual dependencies
- Capture bidirectional causality

**Trade-off**: Slightly less clear progression

### Choosing Between

**Use acyclic** when:
- Teaching or learning
- Clear prerequisites exist
- Linear progression important

**Use cyclic** when:
- Concepts equally fundamental
- Bidirectional relationships important
- Research or reference materials

Most real knowledge graphs use both: acyclic in places, cyclic elsewhere.

---

## Link Density

### Sparse Graphs

Few connections between concepts:

```
Average links per concept: 0.5-1.5
Result: Concepts feel isolated
```

**Problem**: Hard to navigate, discovery difficult

**Solution**: Add more cross-references

### Dense Graphs

Many connections between concepts:

```
Average links per concept: 8+
Result: Everything links to everything
```

**Problem**: Confusing, hard to follow main ideas

**Solution**: Be selective; link only truly related concepts

### Goldilocks Zone

Moderate connectivity:

```
Average links per concept: 2-4
Result: Clear relationships, not overwhelming
```

**Target**: Aim for 2-4 outgoing links per concept

### Calculating Density

```bash
# Count total links
grep -r "\[.*\](.*.md#" docs/ | wc -l

# Count concepts
python3 src/mem_graph.py --root docs headers --all | wc -l

# Average = total_links / total_concepts
```

---

## Cross-Cutting Concerns

### Multiple Dimensions

Concepts might belong in multiple places:

Example: "Neural Network Training"
- Belongs under: Neural Networks
- Belongs under: Optimization
- Belongs under: Implementation

### Solution 1: Multiple Files

Create copies or summaries:

```
docs/neural-networks/training.md
docs/optimization/nn-training.md
```

Both link to each other.

### Solution 2: Taxonomy File

Create index linking across dimensions:

```markdown
## By Algorithm Type

- [Decision Trees](./ml/decision-trees.md)
- [Neural Networks](./ml/neural-networks.md)

---

## By Use Case

- [Classification](./applications/classification.md)
- [Regression](./applications/regression.md)
```

### Solution 3: Conceptual Map

Explicitly show the multiple categorizations:

```markdown
## Training Methods

By algorithm: [Backpropagation](./algorithms.md#backpropagation)
By architecture: [RNN Training](./architectures/rnn.md#training)
By domain: [Vision Model Training](./domains/vision.md#training)
```

---

## Narrative Structure

### Linear Reading

Some concepts should work as linear narrative:

```
[Introduction](#intro) → [Theory](#theory) → 
[Practice](#practice) → [Advanced](#advanced)
```

Concepts link in order for sequential reading.

### Non-Linear Navigation

Others optimize for jumping to concepts:

```
[Main Concept](#main)
  ├─ Related A
  ├─ Related B
  └─ Related C
```

Readers can access any direction from main.

### Hub-and-Spoke

Central concept with many spokes:

```
[Core Concept](#core)
├─ [Background](#background)
├─ [Application 1](#app1)
├─ [Application 2](#app2)
└─ [Deep Dive](#deep)
```

### Creating Reading Paths

Document recommended reading orders:

```markdown
## Recommended Reading Path

If you're new:
1. [Getting Started](./getting-started.md#start)
2. [Fundamentals](./fundamentals.md#fundamentals)
3. [First Example](./examples.md#first-example)

If you have ML background:
1. [Architecture Overview](./architecture.md#overview)
2. [Training Details](./training.md#details)
```

---

## Integration Points

### Connecting Independent Domains

Link between separate knowledge areas:

```
Math Domain: [Linear Algebra](./math/linear-algebra.md#vectors)
     ↓ links to
ML Domain: [Vector Representation](./ml/vectors.md#representation)
     ↓ links to
Vision Domain: [Image Vectors](./vision/embeddings.md#image-vectors)
```

Bridge concepts connect domains.

### Taxonomy Concepts

High-level concepts linking to multiple domains:

```markdown
## Optimization

Used in [Machine Learning](./ml/training.md#optimization)
Used in [Operations Research](./operations/optimization.md#optimization)
Mathematical basis: [Calculus](./math/calculus.md#optimization)
```

---

## Consistency Principles

### Naming

Use consistent conventions:

```
✓ [Backpropagation Algorithm](./file.md#backpropagation-algorithm)
✓ [Gradient Descent Algorithm](./file.md#gradient-descent-algorithm)
✗ [Backprop](./file.md#backprop)
✗ [How Gradient Descent Works](./file.md#gradient-descent)
```

See [Format](./format.md#header-naming-conventions) for details.

### Link Text

Use descriptive, consistent link text:

```
✓ See [Backpropagation](./file.md#backpropagation)
✓ Related: [Gradient Descent](./file.md#gradient-descent)
✗ [click here](./file.md#backpropagation)
✗ [thing](./file.md#gradient-descent)
```

### File Organization

Keep organization consistent:

```
✓ docs/ml/concepts.md, docs/ml/algorithms.md
✓ docs/math/linear-algebra.md, docs/math/calculus.md
✗ docs/ml-concepts.md, docs/math_stuff.md
```

---

## Scalability Considerations

### Small Graphs (< 100 concepts)

Flat structure fine:

```
docs/
  ├── concepts.md
  ├── algorithms.md
  └── applications.md
```

### Medium Graphs (100-1000 concepts)

Add subdirectories:

```
docs/
  ├── fundamentals/
  ├── intermediate/
  └── advanced/
```

### Large Graphs (1000+ concepts)

Multi-level organization:

```
docs/
  ├── foundations/
  │   ├── math/
  │   └── cs-basics/
  ├── algorithms/
  │   ├── sorting/
  │   ├── graphs/
  │   └── dp/
  └── applications/
      ├── web/
      └── systems/
```

See [Scalability](./scalability.md#scalability) for performance considerations.
