## CLI Reference

Complete reference for all md-graph command-line operations.

---

## Invocation

All commands use this base pattern:

```bash
python3 src/mem_graph.py --root docs [command] [options]
```

Where:
- `--root docs`: Path to documentation root directory
- `command`: Operation to perform (headers, view, graph, check)
- `options`: Command-specific parameters

Run without arguments to see help:

```bash
python3 src/mem_graph.py --help
```

---

## Headers Command

List all block headers (node IDs) in a file or all files.

### List headers in single file:

```bash
python3 src/mem_graph.py --root docs headers --file concepts.md
```

Output:
```
concepts.md
  - Machine Learning
  - Neural Networks
  - Training Data
```

### List headers in all files:

```bash
python3 src/mem_graph.py --root docs headers --all
```

Output:
```
concepts.md
  - Machine Learning
  - Neural Networks
  - Training Data
math.md
  - Linear Algebra
  - Calculus
process.md
  - Data Validation
  - Backpropagation
```

### List headers from specific file (full paths):

```bash
python3 src/mem_graph.py --root docs headers --file path/to/file.md
```

Useful for:
- Understanding file contents
- Finding exact header names for queries
- Listing all concepts in knowledge graph

---

## View Command

Display a single block's content.

### By file and header:

```bash
python3 src/mem_graph.py --root docs view --file concepts.md --header "Neural Networks"
```

### By node ID:

```bash
python3 src/mem_graph.py --root docs view --id concepts.md#neural-networks
```

Output includes:
- Full block text
- All links found in block
- Node ID

Useful for:
- Reading specific concepts
- Checking link accuracy
- Validating content

---

## Graph Command

Explore the graph structure around a concept.

### Show neighbors (connected concepts):

```bash
python3 src/mem_graph.py --root docs graph --header "Machine Learning"
```

Output:
```
NODE: concepts.md#machine-learning
  OUT (linked from ML): [Neural Networks, Training Data]
  IN (linking to ML): [Backpropagation]
```

### Show with depth (multi-hop neighbors):

```bash
python3 src/mem_graph.py --root docs graph --header "Machine Learning" --depth 2
```

Depth:
- `--depth 1`: Direct neighbors only (default)
- `--depth 2`: Neighbors and their neighbors
- `--depth 3+`: Further expansion

### Graph from node ID:

```bash
python3 src/mem_graph.py --root docs graph --id concepts.md#machine-learning --depth 2
```

### Export as JSON (machine-readable):

```bash
python3 src/mem_graph.py --root docs graph --header "Concept" --format json
```

Output:
```json
{
  "node": "concepts.md#concept",
  "outgoing": ["file1.md#node1", "file2.md#node2"],
  "incoming": ["file3.md#node3"]
}
```

Useful for:
- Understanding knowledge structure
- Finding related concepts
- Building visualizations
- Detecting isolated nodes

---

## Check Command

Validate the entire graph structure.

### Run validation:

```bash
python3 src/mem_graph.py --root docs check
```

Checks performed:
- All links point to existing headers
- No broken references
- No duplicate node IDs
- Link syntax validity

Output:
```
Checking docs/...
✓ All links valid (847 blocks, 2301 links)
```

Or with errors:

```
✗ Found 3 errors:
  concepts.md:15: Link [Neural Nets](./concepts.md#neural-nets) - header not found
  process.md:42: Link [Missing](./missing.md#concept) - file not found
  math.md:8: Invalid link syntax: [Text}(file.md#concept)
```

### Check specific file:

```bash
python3 src/mem_graph.py --root docs check --file concepts.md
```

Returns validation status for single file only.

### Strict mode (treat warnings as errors):

```bash
python3 src/mem_graph.py --root docs check --strict
```

Useful for:
- Pre-commit validation
- CI/CD pipelines
- Catching broken links early
- Quality assurance

See [Validation](./validation.md#validation) for error interpretation.

---

## Common Workflows

### Find all concepts mentioning "optimization":

```bash
grep -r "optimization" docs/ --include="*.md" | cut -d: -f1 | sort -u
```

Then view each file:

```bash
python3 src/mem_graph.py --root docs headers --file optimization-concepts.md
```

### Check graph consistency before committing:

```bash
python3 src/mem_graph.py --root docs check && echo "✓ Graph OK" || echo "✗ Fix errors"
```

### Find isolated concepts (no links):

```bash
python3 src/mem_graph.py --root docs graph --header "Concept" | grep "OUT (linked"
```

If empty, concept has no outgoing links.

### Explore related concepts (depth 3):

```bash
python3 src/mem_graph.py --root docs graph --id concepts.md#start-concept --depth 3
```

### Generate concept inventory:

```bash
python3 src/mem_graph.py --root docs headers --all > concept-inventory.txt
```

---

## Exit Codes

- `0`: Success
- `1`: General error (invalid file, missing root)
- `2`: Validation failed (broken links)
- `3`: Invalid command syntax

Useful for scripts:

```bash
python3 src/mem_graph.py --root docs check
if [ $? -eq 0 ]; then
    echo "Graph is valid"
else
    echo "Graph has errors"
fi
```

---

## Performance Notes

- **Small graphs** (< 100 blocks): < 100ms
- **Medium graphs** (100-1000 blocks): < 500ms
- **Large graphs** (1000+ blocks): 1-3 seconds

See [Scalability](./scalability.md#scalability) for performance optimization tips.
