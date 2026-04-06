## Best Practices

Proven patterns and guidelines for writing effective md-graph documentation.

---

## Writing Style

### Be Concise

Aim for clarity in 2-5 sentences:

```markdown
## Neural Networks

Computational models inspired by biological neurons, consisting of
interconnected nodes organized in layers. Each connection has a weight
that determines signal strength. Widely used in deep learning.
```

Not:
```markdown
## Neural Networks

Neural networks are inspired by the biological neural systems found
in animals. They consist of artificial neurons which are simple
mathematical functions. These neurons are connected together through
edges with weights. The weights determine how much influence one
neuron has on another. Neural networks can have multiple layers...
[continues for 20 lines]
```

### Use Active Voice

```
✓ [Backpropagation](#backpropagation) computes gradients efficiently
✗ Gradients are computed by [Backpropagation](#backpropagation)
```

### Define Before Linking

Introduce a concept before linking to related ones:

```markdown
## Classification

Machine learning task of predicting discrete categories.
Related: [Regression](#regression) for continuous prediction
Compare: [Clustering](#clustering) for unsupervised grouping
```

Not:
```markdown
## Classification

See [Regression](#regression) and [Clustering](#clustering).
```

### Link Semantically

Show relationship in link text:

```markdown
## Gradient Descent

Optimization algorithm using [Backpropagation](#backpropagation) to compute updates.
Alternative: [Newton's Method](./optimization.md#newtons-method)
Related: [Momentum](./optimization.md#momentum)
```

Not just:
```markdown
## Gradient Descent

[See this](./optimization.md#backpropagation)
[Or this](./optimization.md#newtons-method)
[Also this](./optimization.md#momentum)
```

---

## Linking Practices

### Link Density

Include 2-4 links per concept ideally:

```markdown
## Concept

Definition. See [Related 1](#related-1).

More explanation. Uses [Related 2](./file.md#related-2).

Consider [Alternative](./file.md#alternative) for trade-offs.

---
```

Three links: good
One link: too isolated
Ten links: overwhelming

### Link Placement

Put links naturally in text:

```
✓ [Backpropagation](#backprop) computes gradients using the [chain rule](./math.md#chain-rule).
✗ Text about gradients. [Backpropagation](#backprop). [Chain rule](./math.md#chain-rule).
```

### Link Freshness

Update links when concepts change:

```
Old (after rename): [Old Name](./file.md#old-name)  ✗
Updated: [New Name](./file.md#new-name)             ✓
```

Run `check` regularly to catch broken links.

### Avoid Over-Linking

Not every mention needs a link:

```
✓ See [Neural Networks](#neural-networks) for details.
✗ See [neural](./file.md#neural) [networks](./file.md#networks) for [details](./file.md#details).
```

Link important concepts, not every word.

### Link to Established Concepts

Only link to concepts that are fully defined:

```
✓ Established: [Backpropagation](./file.md#backpropagation)
✗ Forward reference to non-existent concept (breaks validation)
```

Forward references must eventually be resolved.

---

## Naming Conventions

### Header Names

Use clear, specific names:

```
✓ Backpropagation Algorithm
✓ Gradient Descent Optimization
✓ Cross-Entropy Loss Function

✗ Backprop
✗ Gradient Stuff
✗ Loss
```

Guidelines:
- Be specific (avoids duplicate concepts)
- Use nouns, not verbs
- Avoid articles (the, a, an)
- 2-5 words typically

### File Names

Use descriptive, snake_case names:

```
✓ docs/ml/neural-networks.md
✓ docs/optimization/gradient-descent.md
✓ docs/examples/image-classification.md

✗ docs/ml/nn.md
✗ docs/optimization/gd.md
✗ docs/examples/ex1.md
```

### Directory Structure

Use logical grouping:

```
✓ docs/ml/supervised.md
✓ docs/ml/unsupervised.md
✗ docs/ml_supervised.md
✗ docs/supervised_ml.md
```

Consistent capitalization and structure.

---

## Organization

### File Size

Keep files focused (5-20 concepts per file):

```
✓ docs/ml/neural-networks.md (9 concepts)
✗ docs/ml-everything.md (150+ concepts)
```

Reasons:
- Easier to navigate
- Clearer focus
- Better performance
- Simpler git history

### Directory Depth

Limit nesting (2-3 levels typical):

```
✓ docs/ml/algorithms/gradient-descent.md
✗ docs/ml/core/fundamentals/algorithms/optimization/gradient-descent.md
```

### Taxonomies

Create index files for navigation:

```markdown
## Machine Learning Overview

### Algorithms
- [Supervised Learning](./supervised.md#overview)
- [Unsupervised Learning](./unsupervised.md#overview)

### By Task
- [Classification](./tasks/classification.md)
- [Regression](./tasks/regression.md)
```

See [Examples](./examples.md#research-paper-knowledge-base) for full taxonomy patterns.

---

## Content Patterns

### Prerequisites

Explicitly state what's needed:

```markdown
## Advanced Backpropagation

Prerequisites: [Backpropagation](#backpropagation), [Chain Rule](./math.md#chain-rule)

Advanced techniques for backpropagation in specialized architectures...
```

Not: Assuming reader knows prerequisites implicitly

### Examples

Include concrete examples:

```markdown
## Gradient Descent

Iterative algorithm that updates parameters in direction of negative gradient.

Example:
\`\`\`python
for i in range(iterations):
    gradient = compute_gradient(parameters)
    parameters -= learning_rate * gradient
\`\`\`

See [Backpropagation](#backpropagation) for gradient computation.
```

### Alternatives

Mention related/alternative approaches:

```markdown
## Decision Trees

Tree-based model for classification.
Alternatives: [Neural Networks](./ml.md#neural-networks), [SVM](./ml.md#svm)
```

### Limitations

Be honest about drawbacks:

```markdown
## Simple Linear Regression

Fast and interpretable, but limited to linear relationships.
For non-linearity, see [Polynomial Regression](#polynomial) or [Neural Networks](./ml.md#neural-networks).
```

---

## Maintenance

### Regular Validation

Run weekly:
```bash
python3 src/mem_graph.py --root docs check
```

Catch broken links early.

### Link Audits

Periodically review links:

```bash
python3 src/mem_graph.py --root docs check --strict
```

Find orphaned or weakly connected concepts.

### Refactoring Process

When reorganizing:

1. Plan new structure
2. Create new files
3. Add content
4. Update all cross-links
5. Delete old files
6. Run `check` to validate

### Change Documentation

Record decisions:

```markdown
## Refactoring Log

### 2024-02: Reorganize ML docs

Moved neural network concepts from `fundamentals.md` to `neural-networks.md`
Updated 45 cross-file links
Merged redundant concepts
```

---

## Quality Checklist

Before publishing/committing:

- [ ] Concepts are atomic (one idea per block)
- [ ] Headers use consistent naming
- [ ] Links use descriptive text, not "click here"
- [ ] All links point to valid concepts
- [ ] No orphaned blocks (< 5% acceptable)
- [ ] Average link density 2-4 per concept
- [ ] Related concepts are linked
- [ ] `python3 src/mem_graph.py --root docs check` passes
- [ ] File structure is logical
- [ ] Code examples compile/run
- [ ] Spell check complete

---

## Common Mistakes

### Mistake 1: Too Many Links

```
✗ See [A](#a) and [B](#b) and [C](#c) and [D](#d) and [E](#e) for more info.
✓ For related concepts, see [B](#b) and [C](#c).
```

Overwhelms reader. Limit to most relevant.

### Mistake 2: Forward References

```
✗ Link to non-existent: [Future Concept](./file.md#future-concept)
✓ Create concept first, then link
```

Breaks validation. Create before referencing.

### Mistake 3: Unclear Header Names

```
✗ ## Algorithm
✓ ## Gradient Descent Algorithm
```

Ambiguous. Specific is better.

### Mistake 4: Monolithic Blocks

```
✗ 50-line block covering three topics
✓ Three 5-10 line blocks, linked together
```

Violates atomicity. Split into focused blocks.

### Mistake 5: Dead Links

```
✗ Links never validated, broken over time
✓ Run check regularly, especially before commits
```

Regular validation prevents bit rot.

### Mistake 6: Inconsistent Organization

```
✗ File structure: no clear logic
✓ Consistent grouping by domain/process/etc.
```

Confuses readers. Establish pattern and follow it.

---

## Performance Tips

### For Large Graphs

**Use strict file organization**:
```
docs/
  ├── domain-a/
  ├── domain-b/
  └── domain-c/
```

Rather than flat:
```
docs/
  ├── file1.md
  ├── file2.md
  ├── file3.md
  └── ... (100 files)
```

**Limit link depth in queries**:
```bash
✓ python3 src/mem_graph.py --root docs graph --depth 2
✗ python3 src/mem_graph.py --root docs graph --depth 10
```

**Split huge files**:
```
✗ single-file.md (1000+ concepts)
✓ organized-files/ (100-200 concepts each)
```

See [Scalability](./scalability.md#scalability) for detailed optimization.

---

## Documentation Consistency

### Across Multiple Projects

Maintain consistent patterns:

```
✓ All projects: one concept per block, same naming, same link style
✗ Project A: multiple concepts per block
  Project B: minimal linking
```

Makes switching between projects easier.

### Within Single Project

Document conventions:

```markdown
## Contribution Guidelines

- One concept per block (separated by ---)
- Headers: "Noun Phrase" format
- Links: Descriptive link text only
- Files: snake_case.md naming
- Organization: By domain (math/, ml/, etc.)

See [Format](../docs/format.md) for syntax rules.
See [Best Practices](../docs/best-practices.md) for style.
```

---

## Version Control

### Commit Messages

Be specific about changes:

```
✓ Refactor: Split ml.md into supervised/unsupervised
✗ Update docs
```

### Tracking Renames

When renaming concepts:

```
✓ Update all links atomically: git add, commit
✗ Rename in one file, break links in others
```

### Review Process

Before merging:

1. Check `git diff` for broken links
2. Run `check` on new branch
3. Verify new structures follow conventions
4. Review link additions

See [Workflows](./workflows.md#team-collaboration) for team workflows.
