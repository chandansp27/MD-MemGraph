# Knowledge Graph Markdown - LLM Instructions

## Overview

You are writing structured knowledge graph markdown. Each markdown file represents a collection of interconnected knowledge nodes. Your goal is to create clear, informative content while explicitly marking semantic relationships between concepts.

---

## Core Principles

1. **Natural Writing First**: Write clear, flowing prose. Don't over-structure.
2. **Explicit Connections**: When concepts relate, use wiki-links with explicit relation types.
3. **One Node Per Heading**: Each `#` heading becomes a graph node.
4. **Blocks Separated**: Use `---` to visually separate different concept blocks.

---

## File Structure

### Basic Template

```markdown
# Concept Name

Natural language description of the concept. Write 2-4 sentences explaining
what this is, why it matters, or key characteristics.

When mentioning related concepts, use wiki-links: [[Related Concept | relation_type]]

Additional paragraphs can flow naturally.

---

## Another Concept

More natural writing here. [[First Concept | depends_on]] for functionality.
This approach [[Alternative Concept | differs_from]] in key ways.

---

## Third Concept

Continue adding concepts as needed.
```

---

## Syntax Rules

### 1. Headers (Nodes)

```markdown
# Node Name
```

- Use `#` for top-level concepts (becomes a graph node)
- Use `##` for sub-sections (also becomes a node)
- Keep headers concise: 2-5 words ideal
- Use Title Case for important concepts
- Use sentence case for descriptive sections

**Examples:**
```markdown
# Neural Networks
# Backpropagation Algorithm
# Gradient Descent

## Training Process
## Architecture Variants
```

---

### 2. Block Separators

```markdown
---
```

- Use `---` between major concept blocks
- Creates visual separation
- Helps organize related content
- Use after each major heading's content concludes

---

### 3. Wiki-Links (Semantic Connections)

**Format:** `[[Target Heading | relation_type]]`

**Components:**
- `Target Heading` - The heading you're linking to
- `relation_type` - The type of relationship

**Standard Relation Types:**

| Relation | Meaning | Example |
|----------|---------|---------|
| `depends_on` | Requires or needs | `[[Backpropagation | depends_on]]` |
| `supports` | Provides evidence for | `[[Theory X | supports]]` |
| `implements` | Realizes or executes | `[[Algorithm Y | implements]]` |
| `relates_to` | General association | `[[Similar Concept | relates_to]]` |
| `extends` | Builds upon | `[[Base Method | extends]]` |
| `contradicts` | Disagrees with | `[[Alternative View | contradicts]]` |
| `differs_from` | Contrasts with | `[[Other Approach | differs_from]]` |
| `includes` | Contains as part | `[[Subcomponent | includes]]` |
| `used_by` | Applied by | `[[Application Domain | used_by]]` |
| `requires` | Needs as prerequisite | `[[Prerequisites | requires]]` |

**Reverse Relations (use ~ prefix):**
- `~depends_on` - Is depended on by
- `~supports` - Is supported by
- `~implements` - Is implemented by
- etc.

**Target Resolution (4 ways):**

```markdown
# 1. Global heading lookup (searches entire vault)
[[Attention Mechanisms | depends_on]]

# 2. Same-file heading (# prefix)
[[#Section Below | relates_to]]

# 3. Cross-file reference (file#heading)
[[attention.md#Key Concepts | implements]]

# 4. Explicit path (if needed)
[[../concepts/embeddings.md::Token Budget | requires]]
```

---

### 4. Standard Markdown Links

**Format:** `[Display Text](url or path)`

Use for:
- External URLs: `[Read More](https://example.com)`
- Cross-file navigation: `[See details](./other-file.md)`
- Internal anchors: `[Jump to section](#heading-name)`

**Note:** Standard links are NOT parsed into the knowledge graph. Use wiki-links for graph connections.

---

### 5. Natural Prose

Write naturally between links. Examples:

```markdown
Neural networks are computational models inspired by biological neurons.
They [[Backpropagation | depend_on]] for training. Modern architectures
often [[Attention Mechanisms | implement]] to handle sequential data.

The key advantage is hierarchical learning, which [[Deep Learning Theory | supports]]
the effectiveness of these systems.
```

**Guidelines:**
- Write 2-5 sentences per paragraph
- Explain concepts clearly
- Use wiki-links inline, naturally
- Don't force links into every sentence
- Balance prose with connections (aim for 1-3 links per paragraph)

---

## Complete Examples

### Example 1: Technical Concept

```markdown
# Neural Networks

Neural networks are computational models inspired by biological neurons in the brain.
They consist of interconnected layers of nodes that process information through
weighted connections and activation functions.

The training process [[Backpropagation | depends_on]] to compute gradients and
update weights. Modern architectures [[Attention Mechanisms | implement]] to better
handle sequential and contextual information.

Neural networks [[Traditional Machine Learning | differs_from]] by automatically
learning feature representations rather than requiring manual feature engineering.
This capability [[Deep Learning Success | supports]] in domains like computer
vision and natural language processing.

Key characteristics include:
- Hierarchical feature learning
- Non-linear transformations
- End-to-end trainable architectures

For implementation details, see [PyTorch Documentation](https://pytorch.org/docs/).

---

## Backpropagation

Backpropagation is the fundamental algorithm for training neural networks.
It efficiently computes gradients of the loss function with respect to network
parameters using the chain rule of calculus.

The algorithm [[Gradient Descent | used_by]] to update weights iteratively.
This process [[Automatic Differentiation | requires]] to compute derivatives
efficiently.

Historical note: Backpropagation was independently rediscovered multiple times,
with key contributions in the 1980s making it practical for deep networks.

---

## Attention Mechanisms

Attention mechanisms allow models to focus on relevant parts of input sequences
dynamically. They [[Transformer Architecture | implements]] as a core component
for processing sequential data without recurrence.

This approach [[RNNs | differs_from]] by allowing parallel processing and
capturing long-range dependencies more effectively. The success of attention
[[Modern NLP | supports]] in tasks like machine translation and text generation.

---
```

### Example 2: Research Notes

```markdown
# Retrieval-Augmented Generation

RAG combines language models with external knowledge retrieval. The system
[[Vector Databases | depends_on]] to store and retrieve relevant documents
based on semantic similarity.

This approach [[Fine-tuning | differs_from]] by keeping the base model frozen
and augmenting it with retrieved context. RAG [[Factual Accuracy | supports]]
by grounding generations in retrieved evidence.

Implementation typically involves:
1. Encoding queries and documents into embeddings
2. Retrieving top-k relevant documents
3. Conditioning generation on retrieved context

The technique [[Question Answering Systems | used_by]] and [[Knowledge-Intensive NLP | enables]].

---

## Vector Databases

Vector databases specialize in storing and querying high-dimensional embeddings.
They [[Approximate Nearest Neighbor Search | implement]] for efficient similarity
search at scale.

Common examples include Pinecone, Weaviate, and FAISS. These systems [[RAG | supports]]
and [[Semantic Search Applications | enables]].

Performance [[Traditional Databases | differs_from]] due to optimizations for
vector similarity rather than exact matching.

---
```

### Example 3: Personal Knowledge Notes

```markdown
# Project Planning Methodology

My approach to project planning [[Agile Principles | relates_to]] but adapts
them for solo work. The key is maintaining flexibility while having clear
milestones.

I typically start by defining the core objective, then [[Task Breakdown | depends_on]]
to create actionable steps. This method [[Waterfall Planning | differs_from]]
by allowing iteration and adjustment.

Weekly reviews [[Progress Tracking | implements]] to stay aligned with goals.

---

## Task Breakdown

Breaking large goals into smaller tasks [[Project Planning Methodology | supports]]
by making progress measurable. Each task should be completable in 1-3 hours.

The technique [[Getting Things Done | relates_to]] methodology but simplified
for technical work. I find that [[Time Blocking | combines_with]] task breakdown
creates an effective workflow.

---

## Time Blocking

Dedicating specific time periods to specific tasks [[Deep Work | implements]]
principles. This approach [[Context Switching | contradicts]] by minimizing
interruptions and maintaining focus.

Studies show this method [[Productivity Research | supported_by]] across
multiple domains. It [[Task Breakdown | requires]] as a prerequisite for
effective scheduling.

---
```

---

## Common Patterns

### Pattern 1: Hierarchical Knowledge

```markdown
# Machine Learning

Broad field encompassing multiple approaches. [[Supervised Learning | includes]]
and [[Unsupervised Learning | includes]] as major paradigms.

---

## Supervised Learning

Learning from labeled data. [[Neural Networks | implements]] and [[Decision Trees | implements]]
are common approaches.

---

## Unsupervised Learning

Discovering patterns in unlabeled data. [[Clustering | includes]] and [[Dimensionality Reduction | includes]]
as primary techniques.
```

### Pattern 2: Dependency Chains

```markdown
# Web Application

Modern web app [[Frontend Framework | depends_on]] and [[Backend API | depends_on]]
for functionality.

---

## Frontend Framework

User interface layer [[React | implements]] as the primary library. [[Component Architecture | requires]]
for maintainability.

---

## Backend API

Server-side logic [[RESTful Design | implements]] for communication. [[Database | depends_on]]
for persistence.
```

### Pattern 3: Comparative Analysis

```markdown
# Approach A

First method for solving the problem. [[Traditional Solution | extends]] with
modern improvements.

This approach [[Approach B | differs_from]] in computational efficiency but
[[Approach B | relates_to]] in theoretical foundation.

---

## Approach B

Alternative method [[Approach A | differs_from]] by prioritizing accuracy over speed.
Research shows it [[Benchmark Results | supported_by]] in specific scenarios.
```

---

## What to Avoid

### ❌ Don't: Over-link Every Word

```markdown
# Bad Example
[[Neural]] [[networks]] [[use]] [[neurons]] to [[process]] [[data]].
```

**Why bad:** Too many links, unreadable, loses meaning.

### ✅ Do: Link Key Concepts

```markdown
# Good Example
Neural networks [[Backpropagation | depend_on]] for training and [[Activation Functions | use]]
to introduce non-linearity.
```

---

### ❌ Don't: Use Vague Relations

```markdown
# Bad Example
X [[Y | relates_to]]
Z [[Y | relates_to]]
```

**Why bad:** "relates_to" is too generic, doesn't convey meaning.

### ✅ Do: Use Specific Relations

```markdown
# Good Example
X [[Y | depends_on]]
Z [[Y | contradicts]]
```

---

### ❌ Don't: Create Orphan Sections

```markdown
# Bad Example
Some text about attention.

More text about transformers.
```

**Why bad:** No headers means no graph nodes.

### ✅ Do: Use Headers for Concepts

```markdown
# Good Example

# Attention Mechanisms
Some text about attention.

---

## Transformer Architecture
More text about transformers. [[Attention Mechanisms | implements]]
```

---

### ❌ Don't: Forget Block Separators

```markdown
# Bad Example
# Concept A
Text here.
# Concept B
Text here.
```

**Why bad:** Concepts run together visually.

### ✅ Do: Separate with ---

```markdown
# Good Example
# Concept A
Text here.

---

## Concept B
Text here.
```

---

## Content Guidelines

### Writing Quality

1. **Be Clear**: Write as if explaining to a colleague
2. **Be Concise**: 2-5 sentences per paragraph
3. **Be Accurate**: Verify technical claims
4. **Be Connected**: Link related concepts explicitly

### Coverage

1. **Define First**: Start with what the concept is
2. **Explain Why**: Why it matters or when to use it
3. **Connect**: How it relates to other concepts
4. **Provide Context**: Examples or applications

### Link Density

- **Light**: 0-1 links per paragraph (descriptive content)
- **Medium**: 2-3 links per paragraph (normal)
- **Heavy**: 4+ links per paragraph (conceptual mapping)

**Aim for medium density in most cases.**

---

## Special Cases

### Code Blocks

Code blocks are **completely ignored** by the graph parser:

```python
# This [[Won't Be Parsed | fake_relation]]
def example():
    pass
```

Use code blocks freely for examples without worrying about graph pollution.

### Inline Code

Inline code `[[like this]]` is also ignored. Use it for technical terms.

### Blockquotes

Blockquotes are parsed normally:

```markdown
> According to research, neural networks [[Biological Systems | inspired_by]]
> in their architecture.
```

Links inside blockquotes work.

### Lists

Links in lists work normally:

```markdown
Key dependencies:
- [[Numpy | requires]] for numerical computation
- [[PyTorch | depends_on]] for deep learning
- [[Transformers | implements]] for NLP tasks
```

---

## Checklist for Quality Notes

Before finalizing a markdown file, verify:

- [ ] Every major concept has a header (# or ##)
- [ ] Blocks separated with ---
- [ ] Prose is clear and natural
- [ ] Wiki-links use explicit relations (no plain [[text]])
- [ ] Relation types are appropriate
- [ ] 2-4 links per paragraph (not too sparse, not too dense)
- [ ] No orphan text (all content under a header)
- [ ] Code blocks used for examples
- [ ] Standard links used for external references

---

## Quick Reference Card

```markdown
# Structure
---                                    # Block separator
# Heading                              # Creates graph node
## Sub-heading                         # Also creates node

# Wiki-Links (Graph Connections)
[[Target | relation]]                  # Basic format
[[#Same File | relation]]              # Same file reference
[[file.md#Heading | relation]]         # Cross-file reference
[[/path/file.md::Heading | relation]]  # Explicit path

# Relations
depends_on, supports, implements, relates_to, extends,
contradicts, differs_from, includes, used_by, requires

# Reverse Relations (automatic bidirectional)
~depends_on, ~supports, ~implements, etc.

# Standard Markdown
[Text](url)                            # External link (not graphed)
`inline code`                          # Ignored by parser
```code blocks```                     # Ignored by parser
```

---

## Final Notes

- **Write naturally first**, add structure second
- **Every header is a node**, make them meaningful
- **Every wiki-link is an edge**, make them explicit
- **Block separators are visual**, use them generously
- **Code blocks are safe**, use them for examples

The goal is a readable document that also encodes a rich knowledge graph. Think of the wiki-links as semantic annotations on naturally-flowing prose.

---

## Example Workflow

1. **Start with outline** (headers only)
2. **Fill in prose** (natural writing)
3. **Add wiki-links** (connect concepts)
4. **Add separators** (organize visually)
5. **Review and refine** (check link density)
