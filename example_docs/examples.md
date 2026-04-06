## Examples

Real-world examples of md-graph knowledge bases and how they're structured.

---

## Machine Learning Knowledge Graph

A complete knowledge graph for ML concepts and their relationships.

### File structure:

```
docs/ml/
  ├── fundamentals.md
  ├── neural-networks.md
  ├── optimization.md
  ├── evaluation.md
  └── deployment.md
```

### fundamentals.md excerpt:

```markdown
## Machine Learning Definition

Machine learning is a subset of artificial intelligence that enables
systems to learn from data without being explicitly programmed.

Related fields: [Deep Learning](#deep-learning), [Statistics](#statistics)
Alternative approaches: [Rules-Based Systems](./rules.md#rules-based)

---

## Deep Learning

Deep learning uses neural networks with multiple layers.
See [Neural Networks](./neural-networks.md#neural-networks) for architecture.

---

## Supervised Learning

Learning from labeled examples.
Applications: [Classification](#classification), [Regression](#regression)

---

## Classification

Predicting discrete categories.
Related: [Clustering](#clustering) for unsupervised version
Algorithms: [Decision Trees](./algorithms.md#decision-trees)
```

### neural-networks.md excerpt:

```markdown
## Neural Networks

Computational models inspired by biological neurons.
Foundation for [Deep Learning](#deep-learning)
Training: [Backpropagation](./optimization.md#backpropagation)

---

## Layers

Neural networks stack transformations.
Common types: [Dense Layers](#dense-layers), [Convolutional](#convolutional)

---

## Backpropagation Algorithm

Efficient gradient computation for training.
See [Optimization](./optimization.md#optimization-algorithms)
```

### Query examples:

```bash
# Show all ML concepts
python3 src/mem_graph.py --root docs headers --file ml/fundamentals.md

# Explore from Classification
python3 src/mem_graph.py --root docs graph --file ml/fundamentals.md --header "Classification" --depth 2

# Validate all links
python3 src/mem_graph.py --root docs check
```

---

## Research Paper Knowledge Base

Building knowledge from academic papers.

### File structure:

```
docs/papers/
  ├── _taxonomy.md
  ├── transformers/
  │   ├── attention-is-all-you-need.md
  │   ├── bert.md
  │   └── gpt.md
  └── optimization/
      ├── adam.md
      └── sgd.md
```

### _taxonomy.md:

```markdown
## Foundational Papers

Papers that established core techniques.

1. [Attention Is All You Need](./transformers/attention-is-all-you-need.md#paper-summary)
2. [Adam Optimizer](./optimization/adam.md#overview)

---

## Transformer Architecture

Papers about transformer variations.

- [BERT](./transformers/bert.md#model-architecture)
- [GPT Models](./transformers/gpt.md#gpt-overview)
```

### transformers/attention-is-all-you-need.md:

```markdown
## Paper Summary

Introduces transformer architecture based on self-attention.
Published: 2017 by Vaswani et al.

---

## Self-Attention Mechanism

Core innovation allowing parallelization.
Later refined in [BERT](./bert.md#attention-mechanism)

---

## Positional Encoding

Solution for capturing sequence order without recurrence.
Alternative: [Relative Position Bias](./bert.md#relative-positions)

---

## Multi-Head Attention

Multiple attention mechanisms run in parallel.
Improves representation diversity.
Used in [BERT](./bert.md#bert-architecture)
```

### transformers/bert.md:

```markdown
## BERT Architecture

Bidirectional transformer for pre-training.
Builds on: [Transformer](./attention-is-all-you-need.md#transformer-architecture)
Training approach: [Masked Language Model](#masked-language-model)

---

## Attention Mechanism

Refinement of [Self-Attention](./attention-is-all-you-need.md#self-attention-mechanism)
Adds: [Relative Position Bias](#relative-positions)

---

## Relative Positions

Encodes relative distances instead of absolute positions.
Improves generalization compared to [Positional Encoding](./attention-is-all-you-need.md#positional-encoding)
```

---

## Software Project Documentation

Documenting a distributed system.

### File structure:

```
docs/
  ├── architecture.md
  ├── core/
  │   ├── distributed-system.md
  │   └── consensus.md
  ├── services/
  │   ├── authentication.md
  │   ├── storage.md
  │   └── messaging.md
  └── operations/
      ├── deployment.md
      └── monitoring.md
```

### architecture.md:

```markdown
## System Architecture

Three-tier architecture for scalability.
See [Distributed System](./core/distributed-system.md#architecture) for details.
Components: [Authentication](./services/authentication.md#auth-service)

---

## Design Principles

1. **Scalability**: [Load Balancing](./services/messaging.md#load-balancing)
2. **Reliability**: [Consensus](./core/consensus.md#consensus-algorithms)
3. **Security**: [Authentication](./services/authentication.md#auth-service)
```

### core/distributed-system.md:

```markdown
## Distributed System

Multiple nodes working together.
Communication: [Message Queue](../services/messaging.md#message-queue)
Coordination: [Consensus](./consensus.md#consensus-algorithms)

---

## Node Failure Handling

System continues with node failures.
Uses: [Consensus Algorithms](./consensus.md#raft-consensus)
Recovery: [Replication](../services/storage.md#replication)
```

### services/authentication.md:

```markdown
## Authentication Service

Verifies user identity and issues tokens.
Part of [Architecture](../architecture.md#system-architecture)
Token format: [JWT](./token-management.md#jwt)

---

## Token Management

Lifecycle and validation.
Used by: [Authorization](./authorization.md#authorization-flow)
Revocation: [Token Blacklist](#token-blacklist)
```

---

## Learning Curriculum

Structured learning path with progression.

### File structure:

```
docs/curriculum/
  ├── roadmap.md
  ├── 01-foundations/
  │   ├── intro.md
  │   └── basics.md
  ├── 02-intermediate/
  │   └── concepts.md
  └── 03-advanced/
      └── specialization.md
```

### roadmap.md:

```markdown
## Learning Roadmap

Self-paced curriculum with clear prerequisites.

---

## Level 1: Foundations

Master core concepts first.

- [Introduction](./01-foundations/intro.md#welcome)
- [Basic Concepts](./01-foundations/basics.md#fundamentals)

Prerequisites: None
Duration: 2-3 weeks

---

## Level 2: Intermediate

Build on foundations with practical application.

- [Core Concepts](./02-intermediate/concepts.md#main-topics)

Prerequisites: [Level 1](#level-1-foundations)
Duration: 4-6 weeks

---

## Level 3: Advanced

Specialize in topics of interest.

- [Specialization](./03-advanced/specialization.md#tracks)

Prerequisites: [Level 2](#level-2-intermediate)
```

### 01-foundations/intro.md:

```markdown
## Welcome

Start your learning journey here.
Next: [Basic Concepts](./basics.md#fundamentals)

---

## What You'll Learn

Foundation concepts needed for everything else.
This level covers: [Fundamentals](./basics.md#key-topics)

---

## Study Tips

Effective learning practices.
Use with: [Review Questions](./basics.md#practice)
```

---

## Decision Log

Architecture decisions and their rationale.

### File structure:

```
docs/decisions/
  ├── index.md
  ├── 2024-01/
  │   └── cache-strategy.md
  └── 2024-02/
      └── database-choice.md
```

### index.md:

```markdown
## Architecture Decision Log

Record of important technical decisions and rationale.

---

## January 2024 Decisions

- [Cache Strategy](./2024-01/cache-strategy.md#decision)
  Status: Approved

---

## February 2024 Decisions

- [Database Choice](./2024-02/database-choice.md#decision)
  Status: Approved
```

### 2024-01/cache-strategy.md:

```markdown
## Decision: Caching Strategy

**Date**: January 2024
**Status**: Approved
**Context**: Performance degradation under load

---

## Problem Statement

System slow with high query volume.
Related: [Performance Requirements](../index.md#performance)

---

## Options Considered

1. **Caching Tier**: Trade complexity for speed
2. **Database Optimization**: See [Alternative](../2024-02/database-choice.md#option-2)
3. **Query Reduction**: Architectural change

---

## Decision

Implement Redis caching layer.
Rationale: [Cost-Benefit Analysis](#cost-benefit)

---

## Consequences

- Positive: [Performance Gains](#performance)
- Negative: [Operational Overhead](#operations)

See related decision: [Database Choice](../2024-02/database-choice.md#decision)
```

---

## Query Examples Across Examples

```bash
# ML Knowledge Graph
python3 src/mem_graph.py --root docs graph --header "Neural Networks" --depth 3

# Research Papers
python3 src/mem_graph.py --root docs headers --file papers/transformers/attention-is-all-you-need.md

# Software Documentation
python3 src/mem_graph.py --root docs view --file core/distributed-system.md --header "Distributed System"

# Validation across all examples
python3 src/mem_graph.py --root docs check
```

---

## Best Practices from Examples

1. **Clear file organization**: Group related concepts by directory
2. **Progressive linking**: Connect simple to complex
3. **Cross-reference heavily**: Show relationships between domains
4. **Use taxonomy files**: Create overview/index documents
5. **Validate regularly**: Catch broken links early
6. **Document decisions**: Explain the "why" behind structure

See [Best Practices](./best-practices.md#best-practices) for full guidelines.
