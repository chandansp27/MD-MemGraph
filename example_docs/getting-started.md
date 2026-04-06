## Getting Started

Create your first markdown knowledge graph in five minutes. This guide walks you through the essentials.

---

## Installation

The tool requires Python 3.7+. Check your Python version:

```bash
python3 --version
```

Then verify you have the `mem_graph.py` script in your `src/` directory:

```bash
ls src/mem_graph.py
```

---

## Your First Graph

Create a `docs/` directory if you don't have one:

```bash
mkdir -p docs
```

Create a file `docs/concepts.md`:

```markdown
## Machine Learning

Machine learning is a subset of AI focused on systems that learn from data.
Related: [Neural Networks](#neural-networks) and [Training Data](#training-data).

---

## Neural Networks

Neural networks are computational models inspired by biological neurons.
Built on mathematical foundations: [Linear Algebra](./math.md#linear-algebra).
See also [Machine Learning](#machine-learning).

---

## Training Data

The dataset used to train models. Quality matters: [Data Validation](./process.md#data-validation).
```

Create a file `docs/math.md`:

```markdown
## Linear Algebra

Mathematics of vectors, matrices, and transformations.
Essential for: [Neural Networks](./concepts.md#neural-networks).

---

## Calculus

Derivatives and integrals. Used in: [Backpropagation](./process.md#backpropagation).
```

Create a file `docs/process.md`:

```markdown
## Data Validation

Ensuring training data quality before use.
See [Training Data](./concepts.md#training-data) for context.

---

## Backpropagation

Algorithm for computing gradients in neural networks.
Based on: [Calculus](./math.md#calculus).
```

---

## Validate Your Graph

Run the validation command:

```bash
python3 src/mem_graph.py --root docs check
```

This checks all links are valid and reports any issues. See [Validation](./validation.md#validation) for details.

---

## Explore Your Graph

List all concepts in a file:

```bash
python3 src/mem_graph.py --root docs headers --file concepts.md --all
```

View a specific block:

```bash
python3 src/mem_graph.py --root docs view --file concepts.md --header "Neural Networks"
```

Show all neighbors of a concept:

```bash
python3 src/mem_graph.py --root docs graph --header "Machine Learning" --depth 2
```

---

## Next Steps

Congratulations! You've built your first knowledge graph with 3 files and 6 concepts.

- Read [Format](./format.md#format) to understand all syntax rules
- Check [CLI Reference](./cli-reference.md#cli-reference) for more commands
- Study [Best Practices](./best-practices.md#best-practices) for effective organization
- Explore [Examples](./examples.md#examples) for larger graphs

---

## Common Patterns

**Within-file links** (same file):
```markdown
See [Other Concept](#other-concept)
```

**Cross-file links** (another file):
```markdown
See [Concept](./file.md#concept)
```

**Relative paths** (subdirectories):
```markdown
See [Concept](../subfolder/file.md#concept)
```

For more on links, see [Links](./links.md#links).
